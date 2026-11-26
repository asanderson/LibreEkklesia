"""P0-06 checks: the skeleton runs on the decided stack, and its security settings hold.

Tests run against the production settings (config/settings/test.py). Settings that the
test runner rewrites, such as DEBUG and the database name, are checked on the module or
in a fresh interpreter instead.
"""

import logging
import os
import subprocess
import sys
from pathlib import Path

import pytest
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.tasks import TaskResultStatus
from django_tasks_db.models import DBTaskResult

from ninja.security import django_auth

from config.api import api
from config.settings import production
from core.tasks import ping

BACKEND_DIR = Path(__file__).resolve().parent.parent
STRONG_KEY = "x9!Qv#2Lp$7Rz&4Tn*8Wm^5Kd(3Hb)6Jf+1Gc=0Ys~Ue@Ao%Il"
PRODUCTION_ENV = {
    "DJANGO_SETTINGS_MODULE": "config.settings.production",
    "DJANGO_SECRET_KEY": STRONG_KEY,
    "DJANGO_ALLOWED_HOSTS": "church.example",
    "LIBREEKKLESIA_DATA_DIR": "/data",
}
EXPECTED_CSP = (
    "default-src 'self'; base-uri 'self'; form-action 'self'; "
    "frame-ancestors 'none'; object-src 'none'"
)
PUBLIC_OPERATIONS = {("get", "/api/health")}


def run(args, **env):
    """Run a command in a fresh interpreter with only the given project variables set."""
    clean = {k: v for k, v in os.environ.items() if not k.startswith(("DJANGO_", "LIBREEKKLESIA_"))}
    return subprocess.run(
        args, cwd=BACKEND_DIR, env={**clean, **env}, capture_output=True, text=True, timeout=120,
    )


def run_python(code, **env):
    return run([sys.executable, "-c", code], **env)


# API


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


def test_every_api_operation_requires_sign_in_unless_allowlisted(client):
    # New routes inherit session auth, which also enforces CSRF.
    assert api.auth == [django_auth]
    spec = client.get("/api/openapi.json").json()
    open_operations = {
        (method, path)
        for path, operations in spec["paths"].items()
        for method, operation in operations.items()
        if not operation.get("security")
    }
    assert open_operations <= PUBLIC_OPERATIONS


# Headers and hosts


@pytest.mark.parametrize("path", ["/api/health", "/api/openapi.json", "/no-such-page"])
def test_security_headers_on_every_response(client, path):
    headers = client.get(path, headers={"x-forwarded-proto": "https"}).headers
    assert headers["Content-Security-Policy"] == EXPECTED_CSP
    assert headers["Strict-Transport-Security"] == "max-age=31536000"
    assert headers["X-Content-Type-Options"] == "nosniff"
    assert headers["X-Frame-Options"] == "DENY"
    assert headers["Referrer-Policy"] == "same-origin"
    assert headers["Cross-Origin-Opener-Policy"] == "same-origin"


def test_no_hsts_over_plain_http(client):
    assert "Strict-Transport-Security" not in client.get("/api/health").headers


def test_unknown_hosts_are_refused(client):
    assert client.get("/api/health", HTTP_HOST="evil.example").status_code == 400


# Production settings


def test_production_module_values():
    # pytest-django rewrites settings.DEBUG, so read the module itself.
    assert production.DEBUG is False
    assert production.SILENCED_SYSTEM_CHECKS == ["security.W008", "security.W005", "security.W021"]
    assert production.SECURE_PROXY_SSL_HEADER == ("HTTP_X_FORWARDED_PROTO", "https")


def test_cookies_are_secure_prefixed_and_hidden_from_scripts(settings):
    assert settings.SESSION_COOKIE_NAME == "__Host-sessionid"
    assert settings.CSRF_COOKIE_NAME == "__Host-csrftoken"
    assert settings.SESSION_COOKIE_SECURE is True
    assert settings.CSRF_COOKIE_SECURE is True
    assert settings.SESSION_COOKIE_HTTPONLY is True
    assert (settings.SESSION_COOKIE_SAMESITE, settings.CSRF_COOKIE_SAMESITE) == ("Lax", "Lax")


def test_admin_is_absent_in_production_settings(client, settings):
    assert settings.ADMIN_ENABLED is False
    assert "django.contrib.admin" not in settings.INSTALLED_APPS
    assert client.get("/admin/").status_code == 404


def test_deploy_checks_pass_with_production_settings(tmp_path):
    result = run_python(
        "import django; from django.core.management import call_command;"
        " django.setup(); call_command('check', deploy=True, fail_level='WARNING')",
        **{**PRODUCTION_ENV, "LIBREEKKLESIA_DATA_DIR": str(tmp_path)},
    )
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize(
    ("override", "message"),
    [
        ({"DJANGO_SECRET_KEY": ""}, "Set the DJANGO_SECRET_KEY environment variable."),
        ({"DJANGO_SECRET_KEY": "changeme"}, "DJANGO_SECRET_KEY is too weak"),
        ({"LIBREEKKLESIA_DATA_DIR": ""}, "Set the LIBREEKKLESIA_DATA_DIR environment variable."),
        ({"LIBREEKKLESIA_DATA_DIR": "data"}, "LIBREEKKLESIA_DATA_DIR must be an absolute path."),
        ({"DJANGO_ALLOWED_HOSTS": "*"}, "DJANGO_ALLOWED_HOSTS must name the site's hosts"),
        ({"DJANGO_ALLOWED_HOSTS": " , "}, "DJANGO_ALLOWED_HOSTS must name the site's hosts"),
    ],
)
def test_production_refuses_unsafe_environment(override, message):
    result = run_python("import django; django.setup()", **{**PRODUCTION_ENV, **override})
    assert result.returncode != 0
    assert message in result.stderr


def test_manage_py_defaults_to_production_settings():
    env = {k: v for k, v in PRODUCTION_ENV.items() if k != "DJANGO_SETTINGS_MODULE"}
    result = run(
        [sys.executable, "manage.py", "shell", "-c",
         "from django.conf import settings; print(settings.SETTINGS_MODULE, settings.DEBUG)"],
        **env,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip().splitlines()[-1] == "config.settings.production False"


def test_production_logs_django_warnings_to_stderr():
    logger = logging.getLogger("django")
    assert logger.level == logging.WARNING
    assert any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers)


# Sign-in defaults (wired in D1-01)


def test_sign_in_is_browser_only_and_closed_to_self_signup(client, settings):
    assert settings.HEADLESS_ONLY is True
    assert settings.HEADLESS_CLIENTS == ("browser",)
    assert settings.ACCOUNT_SIGNUP_ENABLED is False
    assert client.get("/_allauth/app/v1/config").status_code == 404


def test_passwords_need_at_least_12_characters():
    with pytest.raises(ValidationError):
        validate_password("short-pw-1")
    validate_password("vestry-lantern-harvest-1957")


# Database and task queue


def test_database_is_one_sqlite_file_on_the_data_volume():
    # The test runner swaps in an in-memory database, so read the configured value fresh.
    result = run_python(
        "from pathlib import Path; from config.settings import production as p;"
        " db = p.DATABASES['default'];"
        " assert db['ENGINE'] == 'django.db.backends.sqlite3', db['ENGINE'];"
        " assert db['NAME'] == Path('/data/libreekklesia.sqlite3'), db['NAME'];"
        " assert db['OPTIONS']['transaction_mode'] == 'IMMEDIATE', db['OPTIONS'];"
        " assert 'journal_mode=WAL' in db['OPTIONS']['init_command'], db['OPTIONS'];"
        " assert 'synchronous=FULL' in db['OPTIONS']['init_command'], db['OPTIONS']",
        **PRODUCTION_ENV,
    )
    assert result.returncode == 0, result.stderr


@pytest.mark.django_db
def test_tasks_are_queued_in_the_database():
    result = ping.enqueue()
    assert result.status == TaskResultStatus.READY
    assert DBTaskResult.objects.filter(id=result.id).exists()


# Whole-project checks


def test_system_checks_pass():
    call_command("check", fail_level="WARNING")


def test_development_settings_enable_the_admin(tmp_path):
    result = run_python(
        "import django; from django.conf import settings; from django.core.management import call_command;"
        " django.setup(); call_command('check', fail_level='WARNING');"
        " assert settings.ADMIN_ENABLED and 'django.contrib.admin' in settings.INSTALLED_APPS",
        DJANGO_SETTINGS_MODULE="config.settings.development",
        LIBREEKKLESIA_DATA_DIR=str(tmp_path),
    )
    assert result.returncode == 0, result.stderr
