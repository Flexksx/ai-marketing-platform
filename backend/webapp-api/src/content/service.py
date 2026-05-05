import src.content.repository as content_repository
from src.content.model import (
    Content,
    ContentCreateRequest,
    ContentListRequest,
    ContentUpdateRequest,
)


async def search(request: ContentListRequest) -> list[Content]:
    return await content_repository.search(request)


async def get(post_id: str) -> Content:
    return await content_repository.get(post_id)


async def create(request: ContentCreateRequest) -> Content:
    return await content_repository.create(request)


async def update(post_id: str, request: ContentUpdateRequest) -> Content:
    return await content_repository.update(post_id, request)
