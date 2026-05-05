from datetime import datetime

import public
from pydantic import BaseModel, ConfigDict, Field

from src.brand.model import ContentPillarType, ContentTypeName
from src.shared.model import ContentChannelName, ContentFormat


@public.add
class AgentGeneratedPostingPlanItem(BaseModel):
    content_pillar_type: ContentPillarType
    content_type: ContentTypeName
    content_format: ContentFormat
    channel: ContentChannelName
    scheduled_at: datetime
    description: str

    model_config = ConfigDict(from_attributes=True)


@public.add
class AgentGeneratedPostingPlanResult(BaseModel):
    plan_items: list[AgentGeneratedPostingPlanItem] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
