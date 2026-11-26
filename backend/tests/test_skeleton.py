"""P0-06 checks: the skeleton runs on the decided stack with production settings."""

import os
import subprocess
import sys
from pathlib import Path

import pytest
from django.core.management import call_command
from django.tasks import TaskResultStatus
from django_tasks_db.models import DBTaskResult

from core.tasks import ping

BACKEND_DIR = Path(__file__).resolve().parent.parent
STRONG_TEST_KEY = "x9!Qv#2Lp$7Rz&4Tn*8Wm^5Kd(3Hb)6Jf+1Gc=0Ys~Ue@Ao%Il"


def run_python(code, **env):
    """Run code in a fresh interpreter, so settings modules load from scratch."""
    clean = {k: v for k, v in os.environ.items() if not k.startswith(("DJANGO_", "LIBREEKKLESIA_"))}
    return subprocess.run(
        [sys.executable, "-c", code],
        cwd=BACKEND_DIR, env={**clean, **env}, capture_output=True, text=True, timeout=120,
    )


def test_openapi_description_is_served(client):
    response = client.get("/api/openapi.json")
    assert response.status_code == 200
    spec = response.json()
    assert spec["info"]["title"] == "LibreEkklesia API"
    assert "/api/health" in spec["paths"]


def test_interactive_docs_page_is_off(client):
    assert client.get("/api/docs").status_code == 404


def test_health_endpoint_answers(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_content_security_policy_allows_only_own_origin(client):
    policy = client.get("/api/health").headers["Content-Security-Policy"]
    assert "default-src 'self'" in policy
    assert "frame-ancestors 'none'" in policy
    assert "object-src 'none'" in policy


def test_admin_is_absent_in_production_settings(client, settings):
    assert settings.ADMIN_ENABLED is False
    assert "django.contrib.admin" not in settings.INSTALLED_APPS
    assert client.get("/admin/").status_code == 404


def test_production_cookies_are_secure_and_hidden_from_scripts(settings):
    assert settings.DEBUG is False
    assert settings.SESSION_COOKIE_SECURE is True
    assert settings.CSRF_COOKIE_SECURE is True
    assert settings.SESSION_COOKIE_HTTPONLY is True


def test_database_is_one_sqlite_file_on_the_data_volume():
    # Read the configured value in a fresh interpreter; the test runner swaps in an in-memory database.
    result = run_python(
        "from pathlib import Path; from config.settings import production as p;"
        " db = p.DATABASES['default'];"
        " assert db['ENGINE'] == 'django.db.backends.sqlite3', db['ENGINE'];"
        " assert db['NAME'] == Path('/data/libreekklesia.sqlite3'), db['NAME']",
        DJANGO_SECRET_KEY=STRONG_TEST_KEY,
        DJANGO_ALLOWED_HOSTS="church.example",
        LIBREEKKLESIA_DATA_DIR="/data",
    )
    assert result.returncode == 0, result.stderr


@pytest.mark.django_db
def test_tasks_are_queued_in_the_database():
    result = ping.enqueue()
    assert result.status == TaskResultStatus.READY
    assert DBTaskResult.objects.filter(id=result.id).exists()


def test_system_checks_pass():
    call_command("check", fail_level="WARNING")


def test_deploy_checks_pass_with_production_settings():
    result = run_python(
        "import django, sys; from django.core.management import call_command;"
        " django.setup(); call_command('check', deploy=True, fail_level='WARNING')",
        DJANGO_SETTINGS_MODULE="config.settings.production",
        DJANGO_SECRET_KEY=STRONG_TEST_KEY,
        DJANGO_ALLOWED_HOSTS="church.example",
    )
    assert result.returncode == 0, result.stderr


def test_production_refuses_to_start_without_a_secret_key():
    result = run_python(
        "import django; django.setup()",
        DJANGO_SETTINGS_MODULE="config.settings.production",
        DJANGO_ALLOWED_HOSTS="church.example",
    )
    assert result.returncode != 0
    assert "Set the DJANGO_SECRET_KEY environment variable." in result.stderr


def test_development_settings_enable_the_admin(tmp_path):
    result = run_python(
        "import django; from django.conf import settings; from django.core.management import call_command;"
        " django.setup(); call_command('check', fail_level='WARNING');"
        " assert settings.ADMIN_ENABLED and 'django.contrib.admin' in settings.INSTALLED_APPS",
        DJANGO_SETTINGS_MODULE="config.settings.development",
        LIBREEKKLESIA_DATA_DIR=str(tmp_path),
    )
    assert result.returncode == 0, result.stderr
