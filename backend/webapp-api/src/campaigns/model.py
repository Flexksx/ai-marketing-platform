from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from lib.model import ContentChannelName


class CampaignState(Enum):
    DRAFT = "DRAFT"
    LIVE = "LIVE"
    PAUSED = "PAUSED"
    ENDED = "ENDED"


class CampaignData(BaseModel):
    name: str | None = None
    goal: str | None = None
    description: str | None = None
    target_audience_ids: list[str] = Field(default_factory=list)
    content_pillar_ids: list[str] = Field(default_factory=list)
    content_ids: list[str] = Field(default_factory=list)
    channels: list[ContentChannelName] = Field(default_factory=list)
    media_urls: list[str] = Field(default_factory=list)
    start_date: datetime | None = None
    end_date: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class CampaignCreateRequest(BaseModel):
    brand_id: str
    data: CampaignData

    model_config = ConfigDict(from_attributes=True)


class CampaignUpdateRequest(BaseModel):
    state: CampaignState | None = None
    data: CampaignData | None = None

    model_config = ConfigDict(from_attributes=True)


class CampaignResponse(BaseModel):
    id: str
    brand_id: str
    state: CampaignState
    data: CampaignData | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CampaignListRequest(BaseModel):
    brand_id: str
    state: CampaignState | None = None
    limit: int | None = Field(default=5, ge=1, le=100)
    offset: int | None = Field(default=0, ge=0)

    model_config = ConfigDict(from_attributes=True)


class Campaign(BaseModel):
    id: str
    brand_id: str
    state: CampaignState
    data: CampaignData | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
