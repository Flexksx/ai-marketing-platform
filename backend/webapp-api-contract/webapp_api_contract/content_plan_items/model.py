from datetime import datetime

from pydantic import BaseModel, ConfigDict

from webapp_api_contract.brand.content_type import ContentTypeName
from webapp_api_contract.content import ContentData
from webapp_api_contract.shared import ContentChannelName, ContentFormat, JobStatus


class ContentPlanItem(BaseModel):
    id: str
    job_id: str
    description: str
    channel: ContentChannelName
    content_type: ContentTypeName
    content_format: ContentFormat
    image_urls: list[str] = []
    scheduled_at: datetime
    content_data: ContentData | None = None
    status: JobStatus = JobStatus.PENDING

    model_config = ConfigDict(from_attributes=True)
