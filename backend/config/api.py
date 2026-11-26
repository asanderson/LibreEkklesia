from ninja import NinjaAPI
from ninja.security import django_auth

from core.api import router as core_router

# The interactive docs page loads scripts from a CDN, so it stays off.
# The OpenAPI description is served at /api/openapi.json.
# Every route needs a signed-in session (with its CSRF check) unless it says auth=None.
api = NinjaAPI(title="LibreEkklesia API", version="0.0.0", docs_url=None, auth=django_auth)
api.add_router("", core_router)
