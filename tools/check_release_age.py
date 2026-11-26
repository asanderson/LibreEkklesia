#!/usr/bin/env python3
"""Check that the release-age delay refuses too-new packages.

Finds a release younger than 7 days from a fast-moving package on each side
(boto3 on PyPI, the TypeScript nightly on npm) and tries to add it to a
throwaway copy of the backend or frontend project. Exits 0 only when every
attempt is refused. A side with no release inside the window is reported as
SKIP, which proves nothing.

Run from anywhere: python3 tools/check_release_age.py
Needs uv, pnpm, npm and network access to PyPI and npm.
"""

import datetime as dt
import json
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WINDOW = dt.timedelta(days=7)
NOW = dt.datetime.now(dt.timezone.utc)


def newest_pypi(name):
    with urllib.request.urlopen(f"https://pypi.org/pypi/{name}/json", timeout=30) as response:
        data = json.load(response)
    uploads = [dt.datetime.fromisoformat(f["upload_time_iso_8601"].replace("Z", "+00:00")) for f in data["urls"]]
    return data["info"]["version"], min(uploads)


def newest_npm_nightly(name):
    def view(field):
        return json.loads(subprocess.run(
            ["npm", "view", name, field, "--json"], capture_output=True, text=True, check=True
        ).stdout)
    version = view("dist-tags")["next"]
    published = view("time")[version]
    return version, dt.datetime.fromisoformat(published.replace("Z", "+00:00"))


def refused(command, project, reason):
    """Run command in a throwaway copy; True only if it fails because of the release-age rule."""
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / project.name
        shutil.copytree(project, work, ignore=shutil.ignore_patterns("node_modules", ".venv"))
        result = subprocess.run(command, cwd=work, capture_output=True, text=True)
        lines = [line.strip() for line in (result.stderr + result.stdout).splitlines() if line.strip()]
        why = next((line for line in lines if reason in line), "")
        return result.returncode != 0 and bool(why), why or (lines[-1] if lines else "")


def check(label, version, published, command, project, reason):
    age = NOW - published
    if age >= WINDOW:
        print(f"SKIP {label} {version}: {age.days} days old, nothing inside the window to test")
        return True
    ok, detail = refused(command, project, reason)
    verdict = "PASS" if ok else "FAIL"
    print(f"{verdict} {label} {version} ({age.days} days old): {detail}")
    return ok


def main():
    version, published = newest_pypi("boto3")
    python_ok = check(
        "PyPI boto3", version, published,
        ["uv", "add", "--no-sync", f"boto3=={version}"], ROOT / "backend", "exclude-newer",
    )
    version, published = newest_npm_nightly("typescript")
    node_ok = check(
        "npm typescript", version, published,
        ["pnpm", "add", "--lockfile-only", f"typescript@{version}"], ROOT / "frontend", "minimumReleaseAge",
    )
    sys.exit(0 if python_ok and node_ok else 1)


if __name__ == "__main__":
    main()
