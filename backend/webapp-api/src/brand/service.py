import builtins

import src.brand.repository as brand_repository
from src.brand.model import (
    Brand,
    BrandCreateRequest,
    BrandSearchRequest,
    BrandUpdateRequest,
)


async def get(brand_id: str) -> Brand:
    return await brand_repository.get(brand_id)


async def search(request: BrandSearchRequest) -> builtins.list[Brand]:
    return await brand_repository.search(request)


async def create(user_id: str, request: BrandCreateRequest) -> Brand:
    return await brand_repository.create(user_id, request)


async def update(brand_id: str, request: BrandUpdateRequest) -> Brand:
    return await brand_repository.update(brand_id, request)


async def remove(brand_id: str) -> Brand:
    return await brand_repository.remove(brand_id)


async def validate_access(brand_id: str, user_id: str) -> bool:
    return await brand_repository.exists_for_user(brand_id, user_id)
