#!/bin/sh
# Start-up for the web container: stop on any failed deploy check (SQLite's FTS5 included),
# bring the database schema up to date, then hand over to Gunicorn.
set -eu
python manage.py check --deploy --fail-level WARNING
python manage.py migrate --noinput
exec gunicorn
