from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from webapp_api_contract.shared import ContentChannelName


class BaseContentGenerationJobUserInput(BaseModel):
    prompt: str = Field(...)
    channel: ContentChannelName = Field(...)
    scheduled_at: datetime = Field(...)

    model_config = ConfigDict(from_attributes=True)


class BaseContentGenerationJobResult(BaseModel):
    channel: ContentChannelName
    scheduled_at: datetime

    model_config = ConfigDict(from_attributes=True)
