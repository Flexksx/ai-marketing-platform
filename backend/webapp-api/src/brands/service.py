import builtins

from lib.db.session_factory import DbSessionFactory
from webapp_api_contract.brands import (
    Brand,
    BrandCreateRequest,
    BrandSearchRequest,
    BrandUpdateRequest,
)
import src.brands.repository as brand_repository


async def get(session_factory: DbSessionFactory, brand_id: str) -> Brand:
    return await brand_repository.get(session_factory, brand_id)


async def search(
    session_factory: DbSessionFactory,
    request: BrandSearchRequest,
) -> builtins.list[Brand]:
    return await brand_repository.search(session_factory, request)


async def create(
    session_factory: DbSessionFactory,
    user_id: str,
    request: BrandCreateRequest,
) -> Brand:
    return await brand_repository.create(session_factory, user_id, request)


async def update(
    session_factory: DbSessionFactory,
    brand_id: str,
    request: BrandUpdateRequest,
) -> Brand:
    return await brand_repository.update(session_factory, brand_id, request)


async def remove(session_factory: DbSessionFactory, brand_id: str) -> Brand:
    return await brand_repository.remove(session_factory, brand_id)


async def validate_access(
    session_factory: DbSessionFactory,
    brand_id: str,
    user_id: str,
) -> bool:
    return await brand_repository.exists_for_user(
        session_factory,
        brand_id,
        user_id,
    )
