from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from webapp_api_contract.brand.model import BrandData


class BrandCreateRequest(BaseModel):
    name: str
    data: BrandData

    model_config = ConfigDict(from_attributes=True)


class BrandSearchRequest(BaseModel):
    user_id: str
    name: str | None = None
    limit: int | None = Field(default=5, ge=1, le=1000)
    offset: int | None = Field(default=0, ge=0)


class BrandResponse(BaseModel):
    id: str
    name: str
    data: BrandData | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BrandUpdateRequest(BaseModel):
    name: str | None = None
    data: BrandData | None = None

    model_config = ConfigDict(from_attributes=True)
