"""Gunicorn settings for the web container (docs/stack-decisions.md, section 7)."""

import os

wsgi_app = "config.wsgi"
# Only Caddy reaches this port: the web service publishes none (compose.yaml).
bind = "0.0.0.0:8000"
# Synchronous workers. Two fit the pilot's small server; GUNICORN_WORKERS changes the number.
worker_class = "sync"
workers = int(os.environ.get("GUNICORN_WORKERS", "2"))
timeout = 30
# The container's file system is read-only; /dev/shm is memory-backed.
worker_tmp_dir = "/dev/shm"
# Errors go to standard error, where Docker keeps them on the server.
errorlog = "-"
