"""Run the task worker, refusing to start a second one.

django-tasks-db warns that several workers on SQLite can run the same job twice, so the bundle
runs exactly one (docs/stack-decisions.md, section 11). The lock file lives on the data volume,
which only one host mounts, and the lock is released when the process exits.
"""

import fcntl

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Run the one task worker (django-tasks-db's db_worker) under a lock on the data volume."

    def handle(self, *args, **options):
        lock_path = settings.DATA_DIR / "worker.lock"
        with open(lock_path, "a") as lock:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                raise CommandError(
                    f"Another task worker holds {lock_path}; only one may run."
                ) from None
            call_command("db_worker")
