import logging

import vozai.domain.campaign.service as campaign_service
import vozai.domain.campaign_generation.repository as campaign_generation_job_repository
import vozai.domain.content.service as content_service
import vozai.domain.content_plan_item.service as content_plan_item_service
from db.session_factory import DbSessionFactory
from vozai.domain.campaign.model import Campaign, CampaignData
from vozai.domain.campaign.schema import CampaignCreateRequest
from vozai.domain.campaign_generation.errors import (
    CampaignGenerationJobCreationFailedException,
    CampaignGenerationJobResultNotFoundException,
    CampaignGenerationJobWorkflowTypeMismatchException,
    ContentPlanItemMissingContentDataException,
)
from vozai.domain.campaign_generation.model import (
    CampaignGenerationJob,
    UserMediaOnlyCampaignGenerationJobUserInput,
)
from vozai.domain.campaign_generation.schema import (
    CampaignCreationAcceptRequest,
    CampaignCreationJobUpdateInput,
    CampaignGenerationJobCreateRequest,
    CampaignGenerationJobWorkflowType,
)
from vozai.domain.content.model import (
    TextOnlyContentData,
    TextWithSingleImageContentData,
)
from vozai.domain.content.schema import ContentCreateRequest
from vozai.domain.content_plan_item.schema import ContentPlanItemUpdateRequest


logger = logging.getLogger(__name__)


async def _hydrate_content_plan_items(
    session_factory: DbSessionFactory,
    job: CampaignGenerationJob,
) -> CampaignGenerationJob:
    if not job.result:
        return job
    job.result.content_plan_items = await content_plan_item_service.search(
        session_factory,
        job.id,
    )
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


async def create(
    session_factory: DbSessionFactory,
    request: CampaignGenerationJobCreateRequest,
) -> CampaignGenerationJob:
    _validate_user_media_only_request(request)

    job = await campaign_generation_job_repository.create(session_factory, request)
    if not job:
        raise CampaignGenerationJobCreationFailedException()
    return job


async def get(
    session_factory: DbSessionFactory,
    job_id: str,
) -> CampaignGenerationJob:
    job = await campaign_generation_job_repository.get(session_factory, job_id)
    return await _hydrate_content_plan_items(session_factory, job)


async def update(
    session_factory: DbSessionFactory,
    job_id: str,
    request: CampaignCreationJobUpdateInput,
) -> CampaignGenerationJob:
    job = await campaign_generation_job_repository.update(
        session_factory,
        job_id,
        request,
    )
    return await _hydrate_content_plan_items(session_factory, job)


async def accept(
    session_factory: DbSessionFactory,
    job_id: str,
    request: CampaignCreationAcceptRequest,
) -> Campaign:
    job = await get(session_factory, job_id)

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

    campaign = await campaign_service.create(session_factory, campaign_request)

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
        await content_service.create(session_factory, post_request)
    return campaign


async def validate_access(
    session_factory: DbSessionFactory,
    job_id: str,
    user_id: str,
) -> bool:
    return await campaign_generation_job_repository.exists_for_user(
        session_factory,
        job_id,
        user_id,
    )


async def update_posting_plan_item(
    session_factory: DbSessionFactory,
    job_id: str,
    item_id: str,
    request: ContentPlanItemUpdateRequest,
) -> CampaignGenerationJob:
    await content_plan_item_service.update(
        session_factory,
        item_id,
        request,
    )
    job = await campaign_generation_job_repository.get(session_factory, job_id)
    return await _hydrate_content_plan_items(session_factory, job)
