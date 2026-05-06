import public
from fastapi import Depends

from vozai.domain.content_plan_item import ContentPlanItem
from vozai.domain.content_plan_item.repository import ContentPlanItemRepository
from vozai.domain.content_plan_item.schema import (
    ContentPlanItemCreateRequest,
    ContentPlanItemUpdateRequest,
)


@public.add
class ContentPlanItemService:
    def __init__(self, repository: ContentPlanItemRepository = Depends()):
        self.repository = repository

    async def search(self, job_id: str) -> list[ContentPlanItem]:
        return await self.repository.search(job_id)

    async def get(self, item_id: str) -> ContentPlanItem:
        return await self.repository.get(item_id)

    async def create(self, request: ContentPlanItemCreateRequest) -> ContentPlanItem:
        return await self.repository.create(request)

    async def create_many(
        self, job_id: str, items: list[ContentPlanItemCreateRequest]
    ) -> list[ContentPlanItem]:
        requests = [item.model_copy(update={"job_id": job_id}) for item in items]
        return await self.repository.create_many(requests)

    async def update(
        self, item_id: str, request: ContentPlanItemUpdateRequest
    ) -> ContentPlanItem:
        return await self.repository.update(item_id, request)

    async def remove(self, item_id: str) -> None:
        await self.repository.remove(item_id)
