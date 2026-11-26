from ninja import Router, Schema

router = Router(tags=["system"])


class Health(Schema):
    status: str


@router.get("/health", response=Health, auth=None)
def health(request):
    return {"status": "ok"}
