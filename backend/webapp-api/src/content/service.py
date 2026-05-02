from lib.db.session_factory import DbSessionFactory
from webapp_api_contract.content import (
    Content,
    ContentCreateRequest,
    ContentListRequest,
    ContentUpdateRequest,
)
from webapp_api_contract.content import repository as content_repository


async def search(
    session_factory: DbSessionFactory,
    request: ContentListRequest,
) -> list[Content]:
    return await content_repository.search(session_factory, request)


async def get(session_factory: DbSessionFactory, post_id: str) -> Content:
    return await content_repository.get(session_factory, post_id)


async def create(
    session_factory: DbSessionFactory,
    request: ContentCreateRequest,
) -> Content:
    return await content_repository.create(session_factory, request)


async def update(
    session_factory: DbSessionFactory,
    post_id: str,
    request: ContentUpdateRequest,
) -> Content:
    return await content_repository.update(session_factory, post_id, request)
