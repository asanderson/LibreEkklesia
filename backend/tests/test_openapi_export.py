"""The browser app's copy of the OpenAPI description must match the live API (P0-07)."""

from core.management.commands.export_openapi import DEFAULT_OUTPUT, render_schema


def test_committed_openapi_description_is_current():
    committed = DEFAULT_OUTPUT.read_text(encoding="utf-8")
    assert committed == render_schema(), (
        "The API changed: run `pnpm run api:generate` in frontend/ and commit the result."
    )
