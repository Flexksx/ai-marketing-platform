import logging

import public
from fastapi import Depends

import vozai.domain.campaign.service as campaign_service
import vozai.domain.content.service as content_service
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
from vozai.domain.campaign_generation.repository import (
    CampaignGenerationJobRepository,
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
import vozai.domain.content_plan_item.service as content_plan_item_service
from vozai.domain.content.schema import ContentCreateRequest
from vozai.domain.content_plan_item.schema import ContentPlanItemUpdateRequest
from vozai.lib.cloudtasks.service import CloudTasksService


logger = logging.getLogger(__name__)


@public.add
class CampaignGenerationJobService:
    def __init__(
        self,
        repository: CampaignGenerationJobRepository = Depends(),
        content_plan_item_repository: ContentPlanItemRepository = Depends(),
        session_factory: DbSessionFactory = Depends(),
        tasks_service: CloudTasksService = Depends(),
    ):
        self.repository = repository
        self.content_plan_item_repository = content_plan_item_repository
        self.session_factory = session_factory
        self.tasks_service = tasks_service

    async def create(
        self, request: CampaignGenerationJobCreateRequest
    ) -> CampaignGenerationJob:
        self.__validate_user_media_only_request(request)

        job = await self.repository.create(request)
        if not job:
            raise CampaignGenerationJobCreationFailedException()
        return job

    async def start(
        self, user_id: str, request: CampaignGenerationJobCreateRequest
    ) -> CampaignGenerationJob:
        job = await self.create(request)
        await self.tasks_service.enqueue_campaign_generation(job.id, user_id)
        logger.info(f"Enqueued campaign generation task for job {job.id}")
        return job

    async def get(self, job_id: str) -> CampaignGenerationJob:
        job = await self.repository.get(job_id)
        return await self.__hydrate_content_plan_items(job)

    async def update(
        self, job_id: str, request: CampaignCreationJobUpdateInput
    ) -> CampaignGenerationJob:
        job = await self.repository.update(job_id, request)
        return await self.__hydrate_content_plan_items(job)

    async def accept(
        self, job_id: str, request: CampaignCreationAcceptRequest
    ) -> Campaign:
        job = await self.get(job_id)

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

        campaign = await campaign_service.create(self.session_factory, campaign_request)

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
                    job_id, content_item.id
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
            await content_service.create(self.session_factory, post_request)
        return campaign

    async def validate_access(self, job_id: str, user_id: str) -> bool:
        return await self.repository.exists_for_user(job_id, user_id)

    async def update_posting_plan_item(
        self,
        job_id: str,
        item_id: str,
        request: ContentPlanItemUpdateRequest,
    ) -> CampaignGenerationJob:
        await self.content_plan_item_repository.update(item_id, request)
        job = await self.repository.get(job_id)
        return await self.__hydrate_content_plan_items(job)

    async def __hydrate_content_plan_items(
        self, job: CampaignGenerationJob
    ) -> CampaignGenerationJob:
        if not job.result:
            return job
        job.result.content_plan_items = await self.content_plan_item_repository.search(
            job.id
        )
        return job

    def __validate_user_media_only_request(
        self, request: CampaignGenerationJobCreateRequest
    ):
        user_input = request.user_input
        if (
            isinstance(user_input, UserMediaOnlyCampaignGenerationJobUserInput)
            and request.workflow_type
            == CampaignGenerationJobWorkflowType.USER_MEDIA_ONLY
            and not user_input.image_urls
        ):
            raise CampaignGenerationJobWorkflowTypeMismatchException(
                "Image URLs are required when workflow type is USER_MEDIA_ONLY"
            )
        return True
