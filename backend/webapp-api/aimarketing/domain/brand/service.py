import builtins

import public
from fastapi import Depends

from aimarketing.domain.brand.model import Brand
from aimarketing.domain.brand.repository import BrandRepository
from aimarketing.domain.brand.schema import (
    BrandCreateRequest,
    BrandSearchRequest,
    BrandUpdateRequest,
)


@public.add
class BrandService:
    def __init__(self, repository: BrandRepository = Depends()):
        self.repository = repository

    async def get(self, brand_id: str) -> Brand:
        return await self.repository.get(brand_id)

    async def search(
        self,
        request: BrandSearchRequest,
    ) -> builtins.list[Brand]:
        return await self.repository.search(request)

    async def create(
        self,
        user_id: str,
        request: BrandCreateRequest,
    ) -> Brand:
        return await self.repository.create(user_id, request)

    async def update(
        self,
        brand_id: str,
        request: BrandUpdateRequest,
    ) -> Brand:
        return await self.repository.update(brand_id, request)

    async def remove(self, brand_id: str) -> Brand:
        return await self.repository.remove(brand_id)

    async def validate_access(self, brand_id: str, user_id: str) -> bool:
        return await self.repository.exists_for_user(brand_id, user_id)
