import src.content_plan_item.repository as content_plan_item_repository
from src.content_plan_item.model import (
    ContentPlanItem,
    ContentPlanItemCreateRequest,
    ContentPlanItemUpdateRequest,
)


async def search(job_id: str) -> list[ContentPlanItem]:
    return await content_plan_item_repository.search(job_id)


async def get(item_id: str) -> ContentPlanItem:
    return await content_plan_item_repository.get(item_id)


async def create(request: ContentPlanItemCreateRequest) -> ContentPlanItem:
    return await content_plan_item_repository.create(request)


async def create_many(
    job_id: str,
    items: list[ContentPlanItemCreateRequest],
) -> list[ContentPlanItem]:
    requests = [item.model_copy(update={"job_id": job_id}) for item in items]
    return await content_plan_item_repository.create_many(requests)


async def update(
    item_id: str, request: ContentPlanItemUpdateRequest
) -> ContentPlanItem:
    return await content_plan_item_repository.update(item_id, request)


async def remove(item_id: str) -> None:
    await content_plan_item_repository.remove(item_id)
