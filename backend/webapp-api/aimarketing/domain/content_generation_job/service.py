import logging

import public
from fastapi import Depends

from aimarketing.domain.content import TextOnlyContentData
from aimarketing.domain.content.schema import ContentCreateRequest
from aimarketing.domain.content.service import ContentService
from aimarketing.domain.content_generation_job.content_type.text_with_single_image import (
    TextWithSingleImageContentGenerationJobResult,
)
from aimarketing.domain.content_generation_job.errors import (
    ContentGenerationJobNoResultException,
    ContentGenerationJobUnsupportedWorkflowTypeException,
)
from aimarketing.domain.content_generation_job.model import ContentGenerationJob
from aimarketing.domain.content_generation_job.repository import (
    ContentGenerationJobRepository,
)
from aimarketing.domain.content_generation_job.schema import (
    ContentGenerationJobCreateRequest,
    ContentGenerationJobSearchRequest,
    ContentGenerationJobUpdateRequest,
)
from aimarketing.lib.cloudtasks.service import CloudTasksService


logger = logging.getLogger(__name__)


@public.add
class ContentGenerationJobService:
    def __init__(
        self,
        repository: ContentGenerationJobRepository = Depends(),
        tasks_service: CloudTasksService = Depends(),
        posts_service: ContentService = Depends(),
    ):
        self.repository = repository
        self.tasks_service = tasks_service
        self.posts_service = posts_service

    async def create(
        self, request: ContentGenerationJobCreateRequest
    ) -> ContentGenerationJob:
        return await self.repository.create(request)

    async def get(self, job_id: str) -> ContentGenerationJob:
        return await self.repository.get(job_id)

    async def update(
        self, job_id: str, request: ContentGenerationJobUpdateRequest
    ) -> ContentGenerationJob:
        return await self.repository.update(job_id, request)

    async def search(
        self, request: ContentGenerationJobSearchRequest
    ) -> list[ContentGenerationJob]:
        return await self.repository.search(request)

    async def start(
        self, request: ContentGenerationJobCreateRequest
    ) -> ContentGenerationJob:
        job = await self.create(request)
        await self.tasks_service.enqueue_content_generation(job.id)
        return job

    async def accept(self, job_id: str):
        job = await self.get(job_id)
        result = job.result
        if result is None:
            raise ContentGenerationJobNoResultException(job_id)

        if isinstance(result, TextOnlyContentData):
            raise ContentGenerationJobUnsupportedWorkflowTypeException(
                job_id, job.user_input.workflow_type
            )

        if isinstance(result, TextWithSingleImageContentGenerationJobResult):
            user_input = job.user_input
            request = ContentCreateRequest(
                brand_id=job.brand_id,
                campaign_id=None,
                content_format=result.data.content_format,
                data=result.data,
                channel=result.channel,
                scheduled_at=user_input.scheduled_at,
            )
            return await self.posts_service.create(request)

        return job
