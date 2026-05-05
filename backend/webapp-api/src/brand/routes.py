from fastapi import APIRouter, Depends, File, Form, Query, UploadFile

import src.brand.service as brand_service
from lib.db.session_factory import DbSessionFactory
from lib.supabase_client import (
    SupabaseStorageService,
)
from lib.supabase_client.storage.schema import (
    StorageBucket,
    StorageUploadRequest,
)
from src.auth import get_current_user_id
from src.auth_access import validate_brand_access
from src.brand.model import (
    BrandCreateRequest,
    BrandData,
    BrandResponse,
    BrandSearchRequest,
    BrandUpdateRequest,
)
from src.campaign_generation.routes import (
    router as campaign_creation_router,
)
from src.campaigns.routes import (
    router as campaigns_router,
)
from src.content.routes import (
    router as content_router,
)
from src.content_generation_job.routes import (
    router as content_generation_jobs_router,
)
from src.content_plan_item.routes import (
    router as content_plan_items_router,
)


router = APIRouter(prefix="/brands")
router.include_router(campaigns_router, prefix="/{brand_id}/campaigns")
router.include_router(
    campaign_creation_router,
    prefix="/{brand_id}/campaigns/create",
)
router.include_router(
    content_generation_jobs_router,
    prefix="/{brand_id}/content-generation",
)
router.include_router(content_router, prefix="/{brand_id}/content")
router.include_router(
    content_plan_items_router,
    prefix="/{brand_id}/campaigns/create/{job_id}/content_plan_items",
)


@router.get("", response_model=list[BrandResponse], tags=["Brands"])
async def search(
    user_id: str = Depends(get_current_user_id),
    name: str | None = Query(None),
    limit: int = Query(5, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    session_factory: DbSessionFactory = Depends(),
):
    return await brand_service.search(
        session_factory,
        BrandSearchRequest(
            user_id=user_id,
            name=name,
            limit=limit,
            offset=offset,
        ),
    )


@router.get("/{brand_id}", response_model=BrandResponse, tags=["Brands"])
async def get(
    brand_id: str = Depends(validate_brand_access),
    session_factory: DbSessionFactory = Depends(),
):
    brand = await brand_service.get(session_factory, brand_id)
    return BrandResponse.model_validate(brand)


@router.post("", response_model=BrandResponse, status_code=201, tags=["Brands"])
async def create(
    request: BrandCreateRequest,
    user_id: str = Depends(get_current_user_id),
    session_factory: DbSessionFactory = Depends(),
):
    brand = await brand_service.create(session_factory, user_id, request)
    return BrandResponse.model_validate(brand)


@router.put("/{brand_id}", response_model=BrandResponse, tags=["Brands"])
async def update(
    brand_id: str = Depends(validate_brand_access),
    request_data: str | None = Form(default=None),
    logo_file: UploadFile | None = File(default=None),  # noqa: B008
    session_factory: DbSessionFactory = Depends(),
    supabase_storage_service: SupabaseStorageService = Depends(),
):
    if request_data is None:
        request = BrandUpdateRequest()
    else:
        request = BrandUpdateRequest.model_validate_json(request_data)

    if logo_file is not None:
        logo_content = await logo_file.read()
        upload_result = await supabase_storage_service.upload_public(
            StorageUploadRequest(
                bucket=StorageBucket.BRAND_LOGOS,
                path=f"{brand_id}/{logo_file.filename}",
                content=logo_content,
                content_type=logo_file.content_type,
            )
        )
        if request.data is None:
            request.data = BrandData(logo_url=upload_result.public_url)
        else:
            request.data.logo_url = upload_result.public_url

    brand = await brand_service.update(session_factory, brand_id, request)
    return BrandResponse.model_validate(brand)


@router.delete("/{brand_id}", response_model=BrandResponse, tags=["Brands"])
async def delete(
    brand_id: str = Depends(validate_brand_access),
    session_factory: DbSessionFactory = Depends(),
):
    brand = await brand_service.remove(session_factory, brand_id)
    return BrandResponse.model_validate(brand)
