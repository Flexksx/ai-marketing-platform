import logging

from fastapi import APIRouter, Body, Depends, File, Form, Path, UploadFile

from db.session_factory import DbSessionFactory
from services.client_api.auth.access_validation import validate_brand_access
from services.client_api.campaign_generation_job import get_from_request_form
from vozai.auth import get_current_user_id
from vozai.domain.campaign.schema import CampaignResponse
from vozai.domain.campaign_generation import (
    CampaignCreationAcceptRequest,
    CampaignGenerationJobResponse,
)
import vozai.domain.campaign_generation.service as campaign_generation_job_service
from vozai.lib.cloudtasks.service import CloudTasksService
from vozai.lib.supabase_client import (
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
    session_factory: DbSessionFactory = Depends(),
    tasks_service: CloudTasksService = Depends(),
    supabase_storage_service: SupabaseStorageService = Depends(),
):
    request = await get_from_request_form(
        brand_id, request_data, request_files, supabase_storage_service
    )

    job = await campaign_generation_job_service.start(
        session_factory,
        tasks_service,
        user_id,
        request,
    )

    return CampaignGenerationJobResponse.model_validate(job)


@router.get("/{job_id}", response_model=CampaignGenerationJobResponse)
async def get(
    job_id: str = Path(...),
    brand_id: str = Depends(validate_brand_access),  # noqa: ARG001
    session_factory: DbSessionFactory = Depends(),
):
    job = await campaign_generation_job_service.get(session_factory, job_id)
    return CampaignGenerationJobResponse.model_validate(job)


@router.post("/{job_id}/accept", response_model=CampaignResponse)
async def accept(
    job_id: str = Path(...),
    request: CampaignCreationAcceptRequest = Body(...),  # noqa: B008
    brand_id: str = Depends(validate_brand_access),  # noqa: ARG001
    session_factory: DbSessionFactory = Depends(),
):
    campaign = await campaign_generation_job_service.accept(
        session_factory,
        job_id,
        request,
    )
    return CampaignResponse.model_validate(campaign)
