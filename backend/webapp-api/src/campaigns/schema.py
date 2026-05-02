from datetime import datetime

import public
from pydantic import BaseModel, ConfigDict, Field

from src.campaigns.entity import CampaignState
from webapp_api_contract.campaigns import CampaignData


@public.add
class CampaignCreateRequest(BaseModel):
    brand_id: str
    data: CampaignData

    model_config = ConfigDict(from_attributes=True)


@public.add
class CampaignUpdateRequest(BaseModel):
    state: CampaignState | None = None
    data: CampaignData | None = None

    model_config = ConfigDict(from_attributes=True)


@public.add
class CampaignResponse(BaseModel):
    id: str
    brand_id: str
    state: CampaignState
    data: CampaignData | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


@public.add
class CampaignListRequest(BaseModel):
    brand_id: str
    state: CampaignState | None = None
    limit: int | None = Field(default=5, ge=1, le=100)
    offset: int | None = Field(default=0, ge=0)

    model_config = ConfigDict(from_attributes=True)
