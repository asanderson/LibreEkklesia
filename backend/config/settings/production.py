"""Production settings.

Secrets, hosts and the data volume come from the environment. The settings
refuse to load when any of them is missing or unsafe.
"""

import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403
from .base import DATABASES


def _required(name):
    value = os.environ.get(name, "").strip()
    if not value:
        raise ImproperlyConfigured(f"Set the {name} environment variable.")
    return value


DEBUG = False

# The database lives on the data volume, never inside the container.
DATA_DIR = Path(_required("LIBREEKKLESIA_DATA_DIR"))
if not DATA_DIR.is_absolute():
    raise ImproperlyConfigured("LIBREEKKLESIA_DATA_DIR must be an absolute path.")
DATABASES = {"default": {**DATABASES["default"], "NAME": DATA_DIR / "libreekklesia.sqlite3"}}
MEDIA_ROOT = DATA_DIR / "media"
PUBLIC_SITE_ROOT = DATA_DIR / "site"

SECRET_KEY = _required("DJANGO_SECRET_KEY")
if len(SECRET_KEY) < 50 or len(set(SECRET_KEY)) < 5 or SECRET_KEY.startswith("django-insecure-"):
    raise ImproperlyConfigured("DJANGO_SECRET_KEY is too weak: use at least 50 random characters.")

ALLOWED_HOSTS = [host.strip() for host in _required("DJANGO_ALLOWED_HOSTS").split(",") if host.strip()]
if not ALLOWED_HOSTS or "*" in ALLOWED_HOSTS:
    raise ImproperlyConfigured("DJANGO_ALLOWED_HOSTS must name the site's hosts, not '*'.")

# Caddy terminates HTTPS, redirects plain HTTP, and forwards the original scheme.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 365

SILENCED_SYSTEM_CHECKS = [
    # Caddy redirects HTTP to HTTPS before a request reaches Django.
    "security.W008",
    # A church's domain may host other services, so HSTS stays on this host only.
    "security.W005",
    "security.W021",
]

# Warnings and errors go to standard error, where Docker keeps them on the server.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"stderr": {"class": "logging.StreamHandler"}},
    "loggers": {"django": {"handlers": ["stderr"], "level": "WARNING"}},
}
