import logging

import src.campaign_generation.repository as campaign_generation_job_repository
import src.campaigns.service as campaign_service
import src.content.service as content_service
import src.content_plan_item.service as content_plan_item_service
from src.campaign_generation.errors import (
    CampaignGenerationJobCreationFailedException,
    CampaignGenerationJobResultNotFoundException,
    CampaignGenerationJobWorkflowTypeMismatchException,
    ContentPlanItemMissingContentDataException,
)
from src.campaign_generation.model import (
    CampaignCreationAcceptRequest,
    CampaignCreationJobUpdateInput,
    CampaignGenerationJob,
    CampaignGenerationJobCreateRequest,
    CampaignGenerationJobWorkflowType,
    UserMediaOnlyCampaignGenerationJobUserInput,
)
from src.campaigns.model import Campaign, CampaignCreateRequest, CampaignData
from src.content.model import (
    ContentCreateRequest,
    TextOnlyContentData,
    TextWithSingleImageContentData,
)
from src.content_plan_item.model import ContentPlanItemUpdateRequest


logger = logging.getLogger(__name__)


async def _hydrate_content_plan_items(job: CampaignGenerationJob) -> CampaignGenerationJob:
    if not job.result:
        return job
    job.result.content_plan_items = await content_plan_item_service.search(job.id)
    return job


def _validate_user_media_only_request(
    request: CampaignGenerationJobCreateRequest,
) -> None:
    user_input = request.user_input
    if (
        isinstance(user_input, UserMediaOnlyCampaignGenerationJobUserInput)
        and request.workflow_type == CampaignGenerationJobWorkflowType.USER_MEDIA_ONLY
        and not user_input.image_urls
    ):
        raise CampaignGenerationJobWorkflowTypeMismatchException(
            "Image URLs are required when workflow type is USER_MEDIA_ONLY"
        )


async def create(request: CampaignGenerationJobCreateRequest) -> CampaignGenerationJob:
    _validate_user_media_only_request(request)

    job = await campaign_generation_job_repository.create(request)
    if not job:
        raise CampaignGenerationJobCreationFailedException()
    return job


async def get(job_id: str) -> CampaignGenerationJob:
    job = await campaign_generation_job_repository.get(job_id)
    return await _hydrate_content_plan_items(job)


async def update(
    job_id: str,
    request: CampaignCreationJobUpdateInput,
) -> CampaignGenerationJob:
    job = await campaign_generation_job_repository.update(job_id, request)
    return await _hydrate_content_plan_items(job)


async def accept(
    job_id: str,
    request: CampaignCreationAcceptRequest,
) -> Campaign:
    job = await get(job_id)

    if job.result is None or job.result.content_brief is None:
        raise CampaignGenerationJobResultNotFoundException(job_id)
    description_result = job.result.content_brief

    campaign_data = CampaignData(
        name=description_result.name,
        goal=description_result.goal,
        description=description_result.description,
        target_audience_ids=description_result.target_audience_ids,
        content_pillar_ids=description_result.content_pillar_ids,
        start_date=description_result.start_date,
        end_date=description_result.end_date,
        channels=description_result.channels,
        media_urls=[],
    )
    campaign_request = CampaignCreateRequest(
        brand_id=job.brand_id,
        data=campaign_data,
    )

    campaign = await campaign_service.create(campaign_request)

    if job.result.content_plan_items is None:
        raise CampaignGenerationJobResultNotFoundException(job_id)
    content_items = job.result.content_plan_items

    modifications_by_id = {}
    if request and request.posting_plan_modifications:
        modifications_by_id = {
            mod.item_id: mod for mod in request.posting_plan_modifications
        }

    for content_item in content_items:
        if content_item.content_data is None:
            raise ContentPlanItemMissingContentDataException(
                job_id,
                content_item.id,
            )

        data = content_item.content_data
        scheduled_at = content_item.scheduled_at
        modification = modifications_by_id.get(content_item.id)

        if modification:
            if isinstance(data, TextWithSingleImageContentData):
                data = TextWithSingleImageContentData(
                    caption=(
                        modification.caption
                        if modification.caption is not None
                        else data.caption
                    ),
                    image_url=(
                        modification.image_url
                        if modification.image_url is not None
                        else data.image_url
                    ),
                )
            else:
                data = TextOnlyContentData(
                    caption=(
                        modification.caption
                        if modification.caption is not None
                        else data.caption
                    )
                )
            if modification.scheduled_at is not None:
                scheduled_at = modification.scheduled_at

        post_request = ContentCreateRequest(
            brand_id=job.brand_id,
            campaign_id=campaign.id,
            channel=content_item.channel,
            content_format=content_item.content_format,
            data=data,
            scheduled_at=scheduled_at,
        )
        await content_service.create(post_request)
    return campaign


async def validate_access(job_id: str, user_id: str) -> bool:
    return await campaign_generation_job_repository.exists_for_user(job_id, user_id)


async def update_posting_plan_item(
    job_id: str,
    item_id: str,
    request: ContentPlanItemUpdateRequest,
) -> CampaignGenerationJob:
    await content_plan_item_service.update(item_id, request)
    job = await campaign_generation_job_repository.get(job_id)
    return await _hydrate_content_plan_items(job)
