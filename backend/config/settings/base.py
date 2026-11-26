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
# IMMEDIATE transactions make writers wait for the lock instead of failing;
# synchronous=FULL keeps the last commits (audit entries included) through a power loss.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": DATA_DIR / "libreekklesia.sqlite3",
        "OPTIONS": {
            "transaction_mode": "IMMEDIATE",
            "timeout": 5,
            "init_command": "PRAGMA journal_mode=WAL; PRAGMA synchronous=FULL",
        },
    },
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Staff passwords (the step before the second factor) need at least 12 characters.
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 12},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Sign-in runs only through allauth's headless API for the browser app, with session
# cookies and no tokens. Its URLs are wired in drop 1 (D1-01). Accounts come by
# invitation and admin approval (SEC-10), never by self-signup.
HEADLESS_ONLY = True
HEADLESS_CLIENTS = ("browser",)
ACCOUNT_SIGNUP_ENABLED = False

# Cookies are Secure everywhere (browsers treat localhost as secure, so development works).
# The __Host- prefix stops another site on the church's domain from planting or shadowing them.
SESSION_COOKIE_NAME = "__Host-sessionid"
CSRF_COOKIE_NAME = "__Host-csrftoken"
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Queued and scheduled jobs live in the church's database; exactly one db_worker runs them.
TASKS = {"default": {"BACKEND": "django_tasks_db.DatabaseBackend"}}

# Django's own responses (the API, and the admin in development) allow only the site's own
# origin (security rule 3). Caddy sends the matching policy for the public site and the app (P0-09).
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
