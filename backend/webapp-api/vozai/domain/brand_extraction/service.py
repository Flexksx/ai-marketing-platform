import logging

import public
from fastapi import Depends

import vozai.domain.brand.service as brand_service
from db.session_factory import DbSessionFactory
from vozai.domain.brand.model import Brand
from vozai.domain.brand.schema import BrandCreateRequest
from vozai.domain.brand_extraction.model import (
    BrandGenerationJob,
)
from vozai.domain.brand_extraction.repository import (
    BrandGenerationJobRepository,
)
from vozai.domain.brand_extraction.schema import (
    BrandGenerationJobAcceptRequest,
    BrandGenerationJobCreateRequest,
    BrandGenerationJobUpdateRequest,
)
from vozai.lib.cloudtasks.service import CloudTasksService


logger = logging.getLogger(__name__)


@public.add
class BrandGenerationJobService:
    def __init__(
        self,
        repository: BrandGenerationJobRepository = Depends(),
        session_factory: DbSessionFactory = Depends(),
        tasks_service: CloudTasksService = Depends(),
    ):
        self.repository = repository
        self.session_factory = session_factory
        self.tasks_service = tasks_service

    async def create(
        self, user_id: str, request: BrandGenerationJobCreateRequest
    ) -> BrandGenerationJob:
        return await self.repository.create(user_id, request)

    async def get(self, job_id: str) -> BrandGenerationJob:
        return await self.repository.get(job_id)

    async def update(
        self, job_id: str, request: BrandGenerationJobUpdateRequest
    ) -> BrandGenerationJob:
        return await self.repository.update(job_id, request)

    async def start(
        self, user_id: str, request: BrandGenerationJobCreateRequest
    ) -> BrandGenerationJob:
        job = await self.create(user_id, request)
        await self.tasks_service.enqueue_brand_generation(job.id)
        return job

    async def accept(
        self,
        job_id: str,
        request: BrandGenerationJobAcceptRequest,
    ) -> Brand:
        job = await self.get(job_id)
        brand_input = BrandCreateRequest(name=request.name, data=request.data)
        return await brand_service.create(
            self.session_factory,
            job.user_id,
            brand_input,
        )

    async def validate_access(self, job_id: str, user_id: str) -> bool:
        return await self.repository.exists_for_user(job_id, user_id)
