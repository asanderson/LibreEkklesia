"""System checks that run on every start, `manage.py check` included."""

import sqlite3
from contextlib import closing

from django.core.checks import Error, register

FTS5_HINT = (
    "Search in the member portal and staff admin needs SQLite's FTS5 with the porter tokenizer "
    "(docs/stack-decisions.md, section 11). Use a Python build whose SQLite includes them, such "
    "as the bundle's base image."
)


def fts5_problem():
    """Return what is missing from SQLite's full-text search, or None when everything works."""
    try:
        with closing(sqlite3.connect(":memory:")) as db:
            db.execute(
                "CREATE VIRTUAL TABLE probe USING fts5(body, tokenize = 'porter unicode61')"
            )
            db.executemany(
                "INSERT INTO probe (body) VALUES (?)",
                [("Sunday gatherings",), ("Wednesday study",)],
            )
            stemmed = db.execute(
                "SELECT body FROM probe WHERE probe MATCH 'gather' ORDER BY bm25(probe)"
            ).fetchall()
            prefixed = db.execute(
                "SELECT body FROM probe WHERE probe MATCH 'wedn*'"
            ).fetchall()
    except sqlite3.Error as error:
        return f"SQLite {sqlite3.sqlite_version} cannot run FTS5: {error}"
    if stemmed != [("Sunday gatherings",)] or prefixed != [("Wednesday study",)]:
        return f"SQLite {sqlite3.sqlite_version} returned wrong FTS5 results"
    return None


@register()
def check_sqlite_full_text_search(app_configs, **kwargs):
    problem = fts5_problem()
    return [Error(problem, hint=FTS5_HINT, id="core.E001")] if problem else []
