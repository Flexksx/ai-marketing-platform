from datetime import datetime
from enum import StrEnum

import public
from pydantic import BaseModel, ConfigDict, Field

from aimarketing.domain.content_channel.model import ContentChannelName


@public.add
class CampaignGenerationJobWorkflowType(StrEnum):
    USER_MEDIA_ONLY = "USER_MEDIA_ONLY"
    AI_GENERATED = "AI_GENERATED"
    PRODUCT_LIFESTYLE = "PRODUCT_LIFESTYLE"


@public.add
class BaseCampaignGenerationJobUserInput(BaseModel):
    prompt: str = Field(
        ..., description="User's input about what they want the campaign to be about"
    )
    start_date: datetime = Field(..., description="Campaign start date")
    end_date: datetime = Field(..., description="Campaign end date")
    channels: list[ContentChannelName] = Field(
        ..., description="List of channels the campaign is going to be posted to"
    )

    model_config = ConfigDict(from_attributes=True)
