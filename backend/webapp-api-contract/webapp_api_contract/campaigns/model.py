from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from webapp_api_contract.shared import ContentChannelName


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
