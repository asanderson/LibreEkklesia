"""What the bundle (compose.yaml) relies on from the backend."""

import fcntl
import sqlite3

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError

from core import checks
from core.management.commands import run_worker


def test_sqlite_has_fts5_with_stemming_prefixes_and_ranking():
    # The bundle's image runs this test too (deploy/web.Dockerfile, target "test").
    assert checks.fts5_problem() is None
    assert checks.check_sqlite_full_text_search(None) == []


def test_missing_fts5_stops_the_start(monkeypatch):
    class WithoutFts5:
        def execute(self, sql, *params):
            raise sqlite3.OperationalError("no such module: fts5")

        def close(self):
            pass

    monkeypatch.setattr(checks.sqlite3, "connect", lambda _database: WithoutFts5())
    [error] = checks.check_sqlite_full_text_search(None)
    assert error.id == "core.E001"
    assert "no such module: fts5" in error.msg


def test_media_and_public_site_live_on_the_data_volume(settings):
    assert settings.MEDIA_ROOT == settings.DATA_DIR / "media"
    assert settings.PUBLIC_SITE_ROOT == settings.DATA_DIR / "site"


def test_a_second_task_worker_refuses_to_start(settings, tmp_path, monkeypatch):
    settings.DATA_DIR = tmp_path
    started = []
    monkeypatch.setattr(run_worker, "call_command", lambda name: started.append(name))

    call_command("run_worker")
    assert started == ["db_worker"]

    with open(tmp_path / "worker.lock", "a") as held:
        fcntl.flock(held, fcntl.LOCK_EX | fcntl.LOCK_NB)
        with pytest.raises(CommandError, match="only one may run"):
            call_command("run_worker")
    assert started == ["db_worker"]
