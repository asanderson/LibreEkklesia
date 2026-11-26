"""Production settings. Secrets and hosts come from the environment."""

import os

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403


def _required(name):
    value = os.environ.get(name, "").strip()
    if not value:
        raise ImproperlyConfigured(f"Set the {name} environment variable.")
    return value


DEBUG = False
SECRET_KEY = _required("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = [host.strip() for host in _required("DJANGO_ALLOWED_HOSTS").split(",")]

# Caddy terminates HTTPS, redirects plain HTTP, and forwards the original scheme.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 365

SILENCED_SYSTEM_CHECKS = [
    # Caddy redirects HTTP to HTTPS before a request reaches Django.
    "security.W008",
    # A church's domain may host other services, so HSTS stays on this host only.
    "security.W005",
    "security.W021",
]
