from ninja import NinjaAPI

from core.api import router as core_router

# The interactive docs page loads scripts from a CDN, so it stays off.
# The OpenAPI description is served at /api/openapi.json.
api = NinjaAPI(title="LibreEkklesia API", version="0.0.0", docs_url=None)
api.add_router("", core_router)
