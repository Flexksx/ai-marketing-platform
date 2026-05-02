from fastapi import APIRouter
from scalar_fastapi import Layout, Theme, get_scalar_api_reference


router = APIRouter()


@router.get("/docs", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url="/openapi.json",
        title="Voisso Client API",
        theme=Theme.DEEP_SPACE,
        layout=Layout.MODERN,
    )
