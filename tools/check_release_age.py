#!/usr/bin/env python3
"""Check that the release-age delay refuses too-new packages.

For each side it finds the newest release published within the last 7 days
of a package that ships almost daily (boto3 on PyPI, TypeScript's nightly
builds on npm), then tries to add that exact version to a throwaway copy of
the backend or frontend project. A side passes only when the tool refuses
the version and names its release-age rule as the reason.

Exit status: 0 when both sides pass, 1 when any side fails, 2 when the check
could not prove anything (no release inside the window, network or tool
error).

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
TIMEOUT = 180  # seconds per tool run


def parse_time(stamp):
    return dt.datetime.fromisoformat(stamp.replace("Z", "+00:00"))


def newest_in_window(published):
    """Return (version, time) of the newest release inside the window, or None."""
    recent = [(when, version) for version, when in published.items() if NOW - when < WINDOW]
    if not recent:
        return None
    when, version = max(recent)
    return version, when


def pypi_releases(name):
    with urllib.request.urlopen(f"https://pypi.org/pypi/{name}/json", timeout=30) as response:
        releases = json.load(response)["releases"]
    return {
        version: min(parse_time(f["upload_time_iso_8601"]) for f in files)
        for version, files in releases.items()
        if files
    }


def npm_releases(name):
    output = subprocess.run(
        ["npm", "view", name, "time", "--json"],
        capture_output=True, text=True, check=True, timeout=TIMEOUT,
    ).stdout
    times = json.loads(output)
    return {v: parse_time(t) for v, t in times.items() if v not in ("created", "modified")}


def refused(command, project, reason):
    """Run command in a throwaway copy; True only if it fails because of the release-age rule."""
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / project.name
        shutil.copytree(project, work, ignore=shutil.ignore_patterns("node_modules", ".venv"))
        result = subprocess.run(command, cwd=work, capture_output=True, text=True, timeout=TIMEOUT)
        lines = [line.strip() for line in (result.stderr + result.stdout).splitlines() if line.strip()]
        why = next((line for line in lines if reason in line), "")
        return result.returncode != 0 and bool(why), why or (lines[-1] if lines else "")


def check(label, releases, make_command, project, reason):
    """Return 'pass', 'fail' or 'inconclusive'."""
    found = newest_in_window(releases)
    if found is None:
        print(f"INCONCLUSIVE {label}: no release in the last {WINDOW.days} days to test")
        return "inconclusive"
    version, when = found
    ok, detail = refused(make_command(version), project, reason)
    hours = int((NOW - when).total_seconds() // 3600)
    print(f"{'PASS' if ok else 'FAIL'} {label} {version} ({hours} hours old): {detail}")
    return "pass" if ok else "fail"


def main():
    try:
        results = [
            check(
                "PyPI boto3", pypi_releases("boto3"),
                lambda v: ["uv", "add", "--no-sync", f"boto3=={v}"],
                ROOT / "backend", "exclude-newer",
            ),
            check(
                "npm typescript", npm_releases("typescript"),
                lambda v: ["pnpm", "add", "--lockfile-only", f"typescript@{v}"],
                ROOT / "frontend", "minimumReleaseAge",
            ),
        ]
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        print(f"INCONCLUSIVE: {type(error).__name__}: {error}")
        sys.exit(2)
    if "fail" in results:
        sys.exit(1)
    sys.exit(0 if all(r == "pass" for r in results) else 2)


if __name__ == "__main__":
    main()
