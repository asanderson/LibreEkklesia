"""Write the API's OpenAPI description for the browser app's generated client."""

import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from ninja.responses import NinjaJSONEncoder

DEFAULT_OUTPUT = settings.BASE_DIR.parent / "frontend" / "src" / "api" / "openapi.json"


def render_schema():
    """The description as stable, reviewable JSON: sorted keys, two-space indent."""
    from config.api import api

    schema = api.get_openapi_schema()
    return json.dumps(schema, cls=NinjaJSONEncoder, indent=2, sort_keys=True) + "\n"


class Command(BaseCommand):
    help = "Write the OpenAPI description to the browser app (frontend/src/api/openapi.json)."

    def add_arguments(self, parser):
        parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)

    def handle(self, *args, output, **options):
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(render_schema(), encoding="utf-8")
        self.stdout.write(f"Wrote {output}")
