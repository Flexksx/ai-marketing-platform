from typing import Any

import public
from httpx import AsyncClient

from webapp_api_contract.brands import (
    BrandCreateRequest,
    BrandNotFoundError,
    BrandResponse,
    BrandSearchRequest,
    BrandUpdateRequest,
)


@public.add
class BrandEndpoints:
    BASE_URL = "/brands"

    def __init__(self, client: AsyncClient):
        self.client = client

    async def search(
        self, query: BrandSearchRequest | None = None
    ) -> list[BrandResponse]:
        query_params = query.model_dump() if query else {}
        response = await self.client.get(self.BASE_URL, params=query_params)
        response.raise_for_status()
        return [self.__to_model(item) for item in response.json()]

    async def create(self, brand: BrandCreateRequest) -> BrandResponse:
        response = await self.client.post(self.BASE_URL, json=brand.model_dump())
        response.raise_for_status()
        return self.__to_model(response.json())

    async def update(
        self,
        brand_id: str,
        update_request: BrandUpdateRequest | None = None,
        logo_file: tuple[str, bytes, str] | None = None,
    ) -> BrandResponse:
        form_data = {}
        if update_request is not None:
            form_data["request_data"] = update_request.model_dump_json(
                exclude_unset=True
            )

        files = {}
        if logo_file is not None:
            files["logo_file"] = logo_file

        response = await self.client.put(
            self.BASE_URL + f"/{brand_id}",
            data=form_data if form_data else None,
            files=files if files else None,
        )
        response.raise_for_status()
        return self.__to_model(response.json())

    async def delete(self, brand_id: str) -> None:
        response = await self.client.delete(self.BASE_URL + f"/{brand_id}")
        response.raise_for_status()

    async def get(self, brand_id: str) -> BrandResponse:
        response = await self.client.get(self.BASE_URL + f"/{brand_id}")
        if response.status_code == 404:
            raise BrandNotFoundError(brand_id)
        response.raise_for_status()
        return self.__to_model(response.json())

    def __to_model(self, data: dict[str, Any]) -> BrandResponse:
        return BrandResponse(**data)
