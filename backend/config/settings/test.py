"""Tests run against the production settings, with test-only values for the secrets."""

import os

os.environ.setdefault("DJANGO_SECRET_KEY", "test-only-not-a-secret")
os.environ.setdefault("DJANGO_ALLOWED_HOSTS", "testserver")

from .production import *  # noqa: E402, F403
