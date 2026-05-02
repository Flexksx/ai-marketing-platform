from datetime import datetime

from pydantic import BaseModel, ConfigDict

from webapp_api_contract.content import ContentData
from webapp_api_contract.shared import ContentChannelName, ContentFormat


class Content(BaseModel):
    id: str
    brand_id: str
    campaign_id: str | None = None
    channel: ContentChannelName
    content_format: ContentFormat
    data: ContentData
    created_at: datetime
    updated_at: datetime
    scheduled_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
