import logging

from fastapi import APIRouter, Body, Depends, File, Form, Path, UploadFile

from services.client_api.auth.access_validation import validate_brand_access
from services.client_api.campaign_generation_job import get_from_request_form
from aimarketing.auth import get_current_user_id
from aimarketing.domain.campaign.schema import CampaignResponse
from aimarketing.domain.campaign_generation import (
    CampaignCreationAcceptRequest,
    CampaignGenerationJobResponse,
    CampaignGenerationJobService,
)
from aimarketing.lib.supabase_client import (
    SupabaseStorageService,
)


router = APIRouter(tags=["Brand Campaign Creation"])


logger = logging.getLogger(__name__)


@router.post(
    "",
    response_model=CampaignGenerationJobResponse,
    status_code=201,
)
async def start(
    user_id: str = Depends(get_current_user_id),
    brand_id: str = Depends(validate_brand_access),
    request_data: str = Form(...),
    request_files: list[UploadFile] = File(default=[]),  # noqa: B008
    campaign_generation_job_service: CampaignGenerationJobService = Depends(),
    supabase_storage_service: SupabaseStorageService = Depends(),
):
    request = await get_from_request_form(
        brand_id, request_data, request_files, supabase_storage_service
    )

    job = await campaign_generation_job_service.start(user_id, request)

    return CampaignGenerationJobResponse.model_validate(job)


@router.get("/{job_id}", response_model=CampaignGenerationJobResponse)
async def get(
    job_id: str = Path(...),
    brand_id: str = Depends(validate_brand_access),  # noqa: ARG001
    service: CampaignGenerationJobService = Depends(),
):
    job = await service.get(job_id)
    return CampaignGenerationJobResponse.model_validate(job)


@router.post("/{job_id}/accept", response_model=CampaignResponse)
async def accept(
    job_id: str = Path(...),
    request: CampaignCreationAcceptRequest = Body(...),  # noqa: B008
    brand_id: str = Depends(validate_brand_access),  # noqa: ARG001
    service: CampaignGenerationJobService = Depends(),
):
    campaign = await service.accept(job_id, request)
    return CampaignResponse.model_validate(campaign)
