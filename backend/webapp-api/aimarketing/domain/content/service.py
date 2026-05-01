import public
from fastapi import Depends

from aimarketing.domain.content.model import Content
from aimarketing.domain.content.repository import ContentRepository
from aimarketing.domain.content.schema import (
    ContentCreateRequest,
    ContentListRequest,
    ContentUpdateRequest,
)


@public.add
class ContentService:
    def __init__(self, repository: ContentRepository = Depends()):
        self.repository = repository

    async def search(self, request: ContentListRequest) -> list[Content]:
        return await self.repository.search(request)

    async def get(self, post_id: str) -> Content:
        return await self.repository.get(post_id)

    async def create(self, request: ContentCreateRequest) -> Content:
        return await self.repository.create(request)

    async def update(self, post_id: str, request: ContentUpdateRequest) -> Content:
        return await self.repository.update(post_id, request)
