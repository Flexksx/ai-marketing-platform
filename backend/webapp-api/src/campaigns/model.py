from datetime import datetime

import public
from pydantic import BaseModel, ConfigDict, Field

from webapp_api_contract.brand_settings import ContentPillarBusinessGoal
from src.campaigns.entity import CampaignState
from webapp_api_contract.shared import ContentChannelName


@public.add
class CampaignData(BaseModel):
    name: str = Field(default="")
    goal: ContentPillarBusinessGoal = Field(
        default=ContentPillarBusinessGoal.INCREASE_CONVERSION
    )
    description: str = Field(default="")
    target_audience_ids: list[str] = Field(default_factory=list)
    content_pillar_ids: list[str] = Field(default_factory=list)
    content_ids: list[str] = Field(default_factory=list)
    channels: list[ContentChannelName] = Field(default_factory=list)
    media_urls: list[str] = Field(default_factory=list)
    start_date: datetime
    end_date: datetime
    model_config = ConfigDict(from_attributes=True)


@public.add
class Campaign(BaseModel):
    id: str
    brand_id: str
    state: CampaignState
    data: CampaignData = Field(default_factory=CampaignData)

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
