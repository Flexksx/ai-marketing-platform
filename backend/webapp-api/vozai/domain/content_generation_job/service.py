import logging

import public
from fastapi import Depends

import vozai.domain.content.service as content_service
from db.session_factory import DbSessionFactory
from vozai.domain.content import TextOnlyContentData
from vozai.domain.content.schema import ContentCreateRequest
from vozai.domain.content_generation_job.content_type.text_with_single_image import (
    TextWithSingleImageContentGenerationJobResult,
)
from vozai.domain.content_generation_job.errors import (
    ContentGenerationJobNoResultException,
    ContentGenerationJobUnsupportedWorkflowTypeException,
)
from vozai.domain.content_generation_job.model import ContentGenerationJob
from vozai.domain.content_generation_job.repository import (
    ContentGenerationJobRepository,
)
from vozai.domain.content_generation_job.schema import (
    ContentGenerationJobCreateRequest,
    ContentGenerationJobSearchRequest,
    ContentGenerationJobUpdateRequest,
)
from vozai.lib.cloudtasks.service import CloudTasksService


logger = logging.getLogger(__name__)


@public.add
class ContentGenerationJobService:
    def __init__(
        self,
        repository: ContentGenerationJobRepository = Depends(),
        tasks_service: CloudTasksService = Depends(),
        session_factory: DbSessionFactory = Depends(),
    ):
        self.repository = repository
        self.tasks_service = tasks_service
        self.session_factory = session_factory

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
            return await content_service.create(self.session_factory, request)

        return job
