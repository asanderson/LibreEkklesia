"""Tests run against the production settings, with test-only values from the environment."""

import os
import tempfile
from pathlib import Path

from django.core.management.utils import get_random_secret_key

os.environ.setdefault("DJANGO_SECRET_KEY", get_random_secret_key())
os.environ.setdefault("DJANGO_ALLOWED_HOSTS", "testserver")
os.environ.setdefault("LIBREEKKLESIA_DATA_DIR", str(Path(tempfile.gettempdir()) / "libreekklesia-test"))

from .production import *  # noqa: E402, F403
