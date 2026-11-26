"""Local development: debug on and Django's built-in admin available."""

import copy

from .base import *  # noqa: F403
from .base import DATA_DIR, INSTALLED_APPS, MIDDLEWARE, TEMPLATES

DEBUG = True
SECRET_KEY = "development-only-not-a-secret"  # noqa: S105
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

ADMIN_ENABLED = True
INSTALLED_APPS = [
    *INSTALLED_APPS,
    "django.contrib.admin",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
MIDDLEWARE = [*MIDDLEWARE, "django.contrib.messages.middleware.MessageMiddleware"]
TEMPLATES = copy.deepcopy(TEMPLATES)
TEMPLATES[0]["OPTIONS"]["context_processors"].append(
    "django.contrib.messages.context_processors.messages"
)
STATIC_URL = "static/"

DATA_DIR.mkdir(parents=True, exist_ok=True)
