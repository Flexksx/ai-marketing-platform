import src.content_plan_item.repository as content_plan_item_repository
from lib.db.session_factory import DbSessionFactory
from webapp_api_contract.content_plan_items import (
    ContentPlanItem,
    ContentPlanItemCreateRequest,
    ContentPlanItemUpdateRequest,
)


async def search(
    session_factory: DbSessionFactory, job_id: str
) -> list[ContentPlanItem]:
    return await content_plan_item_repository.search(session_factory, job_id)


async def get(session_factory: DbSessionFactory, item_id: str) -> ContentPlanItem:
    return await content_plan_item_repository.get(session_factory, item_id)


async def create(
    session_factory: DbSessionFactory,
    request: ContentPlanItemCreateRequest,
) -> ContentPlanItem:
    return await content_plan_item_repository.create(session_factory, request)


async def create_many(
    session_factory: DbSessionFactory,
    job_id: str,
    items: list[ContentPlanItemCreateRequest],
) -> list[ContentPlanItem]:
    requests = [item.model_copy(update={"job_id": job_id}) for item in items]
    return await content_plan_item_repository.create_many(session_factory, requests)


async def update(
    session_factory: DbSessionFactory,
    item_id: str,
    request: ContentPlanItemUpdateRequest,
) -> ContentPlanItem:
    return await content_plan_item_repository.update(
        session_factory,
        item_id,
        request,
    )


async def remove(session_factory: DbSessionFactory, item_id: str) -> None:
    await content_plan_item_repository.remove(session_factory, item_id)
