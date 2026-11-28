"""Check a running bundle from the outside: HTTPS, routes, headers, volumes and the worker.

Run from the repository root after `docker compose up --build --detach` with
LIBREEKKLESIA_HOST=localhost. Uses only the standard library. Exits 1 when a check fails.
"""

from __future__ import annotations

import http.client
import json
import os
import pathlib
import secrets
import ssl
import subprocess
import sys
import tempfile
import time

HOST = "localhost"
DJANGO_CSP = (
    "default-src 'self'; base-uri 'self'; form-action 'self'; "
    "frame-ancestors 'none'; object-src 'none'"
)
HSTS = "max-age=31536000"
RESULTS: list[tuple[bool, str]] = []


def check(ok: bool, label: str) -> None:
    RESULTS.append((ok, label))
    print(("PASS " if ok else "FAIL ") + label, flush=True)


def compose(*args: str, timeout: int = 120) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["docker", "compose", *args], capture_output=True, text=True, timeout=timeout
    )


def fetch(path: str, *, scheme: str = "https", context=None, headers=None, method="GET", body=None):
    if scheme == "https":
        connection = http.client.HTTPSConnection(HOST, 443, context=context, timeout=10)
    else:
        connection = http.client.HTTPConnection(HOST, 80, timeout=10)
    connection.request(method, path, body=body, headers=headers or {})
    response = connection.getresponse()
    body = response.read()
    connection.close()
    return response, body


def local_authority(folder: pathlib.Path) -> ssl.SSLContext:
    """Wait for Caddy's local root certificate and trust only it."""
    root = folder / "root.crt"
    for _ in range(90):
        copy = compose("cp", "caddy:/data/caddy/pki/authorities/local/root.crt", str(root))
        if copy.returncode == 0 and root.exists():
            return ssl.create_default_context(cafile=str(root))
        time.sleep(2)
    raise SystemExit("Caddy's local root certificate never appeared")


def wait_for_health(context: ssl.SSLContext) -> None:
    for _ in range(90):
        try:
            response, _ = fetch("/api/health", context=context)
            if response.status == 200:
                return
        except OSError:
            pass
        time.sleep(2)
    raise SystemExit("https://localhost/api/health never answered 200")


def static_headers_ok(response) -> bool:
    return (
        response.getheader("Content-Security-Policy") == DJANGO_CSP
        and response.getheader("Strict-Transport-Security") == HSTS
        and response.getheader("X-Content-Type-Options") == "nosniff"
        and response.getheader("X-Frame-Options") == "DENY"
        and response.getheader("Referrer-Policy") == "same-origin"
        and response.getheader("Cross-Origin-Opener-Policy") == "same-origin"
        and bool(response.getheader("Permissions-Policy"))
        and response.getheader("Server") is None
    )


def main() -> None:
    with tempfile.TemporaryDirectory() as folder:
        context = local_authority(pathlib.Path(folder))
        wait_for_health(context)

        # Django behind Caddy.
        response, body = fetch("/api/health", context=context)
        check(
            response.status == 200 and json.loads(body) == {"status": "ok"},
            "https://localhost/api/health answers with a certificate from Caddy's authority",
        )
        check(
            response.getheader("Content-Security-Policy") == DJANGO_CSP,
            "Django sends its content security policy through Caddy",
        )
        check(
            response.getheader("Strict-Transport-Security") == HSTS,
            "Django sees HTTPS behind Caddy (it adds HSTS only on secure requests)",
        )
        response, _ = fetch("/api/health", context=context, headers={"X-Forwarded-Proto": "http"})
        check(
            response.getheader("Strict-Transport-Security") == HSTS,
            "Caddy replaces a client's X-Forwarded-Proto instead of passing it on",
        )
        response, _ = fetch("/api/health", scheme="http")
        check(
            response.status in (301, 308)
            and response.getheader("Location") == "https://localhost/api/health",
            f"plain HTTP redirects to HTTPS ({response.status})",
        )

        # The browser app.
        response, body = fetch("/app/", context=context)
        check(
            response.status == 200 and b'<div id="app">' in body,
            "/app/ serves the browser app",
        )
        check(static_headers_ok(response), "/app/ carries the security headers")
        response, body = fetch("/app/some/deep/route", context=context)
        check(
            response.status == 200 and b'<div id="app">' in body,
            "a deep link under /app/ gets the app page",
        )
        response, _ = fetch("/app/assets/missing.js", context=context)
        check(response.status == 404, "a missing build file is a 404, not the app page")
        check(
            response.getheader("Content-Security-Policy") == DJANGO_CSP,
            "error responses from Caddy carry the security headers too",
        )
        response, _ = fetch(
            "/api/health", context=context, method="POST", body=b"x" * 1_500_000,
            headers={"Content-Type": "application/octet-stream"},
        )
        check(response.status == 413, f"Caddy refuses an API request body over 1 MB ({response.status})")
        response, _ = fetch("/app", context=context)
        check(
            response.status in (301, 308) and response.getheader("Location") == "/app/",
            "/app redirects to /app/",
        )
        response, body = fetch("/app/licenses.md", context=context)
        check(
            response.status == 200
            and response.getheader("Content-Type") == "text/plain; charset=utf-8"
            and b"vue" in body,
            "/app/licenses.md shows the bundled packages' license notices as text",
        )

        # The generated public site, written by the web container. A uniquely named probe page
        # leaves anything already published alone.
        probe = f"smoke-test-{secrets.token_hex(8)}.html"
        page = "<!doctype html><title>Site</title><p>Published by the web container</p>"
        write = compose(
            "exec", "-T", "web", "python", "-c",
            f"import pathlib; pathlib.Path('/data/site/{probe}').write_text({page!r})",
        )
        response, body = fetch(f"/{probe}", context=context)
        compose("exec", "-T", "web", "rm", "-f", f"/data/site/{probe}")
        check(
            write.returncode == 0
            and response.status == 200
            and b"Published by the web container" in body,
            "Caddy serves the public site that the web container writes",
        )
        check(static_headers_ok(response), "the public site carries the security headers")
        response, _ = fetch("/favicon.ico", context=context)
        check(response.status == 204, "/favicon.ico answers with no content until the site has one")
        touch = compose("exec", "-T", "caddy", "touch", "/srv/site/probe")
        check(
            touch.returncode != 0 and "Read-only file system" in touch.stderr,
            "Caddy mounts the public site volume read-only",
        )

    # Inside the web image.
    deploy_check = compose(
        "exec", "-T", "web", "python", "manage.py", "check", "--deploy", "--fail-level", "WARNING"
    )
    version = compose(
        "exec", "-T", "web", "python", "-c", "import sqlite3; print(sqlite3.sqlite_version)"
    )
    check(
        deploy_check.returncode == 0 and "no issues" in deploy_check.stdout,
        f"the deploy check passes inside the web image, FTS5 included (SQLite {version.stdout.strip()})",
    )
    user = compose("exec", "-T", "web", "id", "-u")
    check(user.stdout.strip() == "10001", "the web container runs as a non-root user")
    caddy_user = compose("exec", "-T", "caddy", "id", "-u")
    check(caddy_user.stdout.strip() == "10002", "Caddy runs as a non-root user")
    adapted = compose("exec", "-T", "caddy", "caddy", "adapt", "--config", "/etc/caddy/Caddyfile")
    limits = {"max_size": [], "request_buffers": []}

    def collect(node):
        if isinstance(node, dict):
            for key, value in node.items():
                if key in limits:
                    limits[key].append(value)
                collect(value)
        elif isinstance(node, list):
            for item in node:
                collect(item)

    if adapted.returncode == 0:
        collect(json.loads(adapted.stdout))
    check(
        len(limits["max_size"]) == 1
        and len(limits["request_buffers"]) == 1
        and limits["request_buffers"][0] > limits["max_size"][0],
        f"Caddy holds a whole API request body before Gunicorn sees any of it {limits}",
    )
    baked = subprocess.run(
        ["docker", "run", "--rm", "--entrypoint", "find", "libreekklesia-caddy:dev",
         "/data", "/config", "/tmp", "-type", "f"],
        capture_output=True, text=True, timeout=120,
    )
    check(
        baked.returncode == 0 and not baked.stdout.strip(),
        "the Caddy image holds no certificates or keys",
    )
    database = compose("exec", "-T", "web", "test", "-f", "/data/libreekklesia.sqlite3")
    check(database.returncode == 0, "the database file is on the data volume")
    listing = compose("ps", "--format", "json", "web")
    containers = []
    for line in listing.stdout.splitlines():
        if line.strip():
            entry = json.loads(line)
            containers += entry if isinstance(entry, list) else [entry]
    published = [
        port
        for container in containers
        for port in container.get("Publishers") or []
        if port.get("PublishedPort")
    ]
    check(
        listing.returncode == 0 and len(containers) == 1 and not published,
        f"the web container publishes no ports {published}",
    )
    roundtrip = compose(
        "exec", "-T", "web", "python", "-c",
        "import django, time\n"
        "django.setup()\n"
        "from core.tasks import ping\n"
        "result = ping.enqueue()\n"
        "deadline = time.monotonic() + 60\n"
        "while not result.is_finished and time.monotonic() < deadline:\n"
        "    time.sleep(1)\n"
        "    result.refresh()\n"
        "print(result.status, result.return_value if result.is_finished else None)\n",
        timeout=90,
    )
    check(
        roundtrip.stdout.split() == ["SUCCESSFUL", "pong"],
        f"the task worker runs a queued task ({roundtrip.stdout.strip() or roundtrip.stderr.strip()[-200:]})",
    )
    web_logs = compose("logs", "--no-color", "web")
    errors = [line for line in web_logs.stdout.splitlines() if "[ERROR]" in line]
    check(not errors, f"the web container logged no errors {errors[:3]}")
    try:
        second = compose("run", "--rm", "--no-deps", "-T", "worker", timeout=90)
        refused = second.returncode != 0 and "only one may run" in second.stderr
    except subprocess.TimeoutExpired:
        refused = False
    check(refused, "a second task worker refuses to start")

    failed = [label for ok, label in RESULTS if not ok]
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if os.environ.get("GITHUB_ACTIONS"):
        lines = "%0A".join(("PASS " if ok else "FAIL ") + label for ok, label in RESULTS)
        print(f"::notice title=Bundle smoke test ({len(RESULTS) - len(failed)} of {len(RESULTS)} passed)::{lines}")
        for label in failed[:10]:
            print(f"::error title=Bundle smoke test::{label}")
    if summary:
        with open(summary, "a", encoding="utf-8") as out:
            out.write("### Bundle smoke test\n\n")
            out.writelines(f"- {'PASS' if ok else 'FAIL'} {label}\n" for ok, label in RESULTS)
    print(f"{len(failed)} failed" if failed else "all checks passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
