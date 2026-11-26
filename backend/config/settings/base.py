"""Settings shared by every environment.

production.py adds secrets, hosts and HTTPS settings; development.py adds the
built-in admin; test.py runs the tests against the production settings.
"""

import os
from pathlib import Path

from django.utils.csp import CSP

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# The data volume holds the church's database file (and, later, media and backups).
DATA_DIR = Path(os.environ.get("LIBREEKKLESIA_DATA_DIR", BASE_DIR / "var"))

# The staff admin is the project's own app; Django's built-in admin is for development only.
ADMIN_ENABLED = False

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "allauth",
    "allauth.account",
    "allauth.headless",
    "django_tasks_db",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.csp.ContentSecurityPolicyMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
            ],
        },
    },
]

# One SQLite file per church. WAL lets readers work while one writer writes;
# IMMEDIATE transactions make writers wait for the lock instead of failing.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": DATA_DIR / "libreekklesia.sqlite3",
        "OPTIONS": {
            "transaction_mode": "IMMEDIATE",
            "timeout": 5,
            "init_command": "PRAGMA journal_mode=WAL; PRAGMA synchronous=NORMAL",
        },
    },
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Sign-in runs only through allauth's headless API. Its URLs are wired in drop 1 (D1-01).
HEADLESS_ONLY = True

# Queued and scheduled jobs live in the church's database; exactly one db_worker runs them.
TASKS = {"default": {"BACKEND": "django_tasks_db.DatabaseBackend"}}

# Everything loads from the site's own origin (security rule 3).
SECURE_CSP = {
    "default-src": [CSP.SELF],
    "base-uri": [CSP.SELF],
    "form-action": [CSP.SELF],
    "frame-ancestors": [CSP.NONE],
    "object-src": [CSP.NONE],
}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
