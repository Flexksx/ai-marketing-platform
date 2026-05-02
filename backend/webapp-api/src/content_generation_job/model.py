from datetime import datetime

from pydantic import BaseModel, ConfigDict

from webapp_api_contract.content_generation import (
    ContentGenerationJobResult,
    ContentGenerationJobUserInput,
)
from webapp_api_contract.shared import ContentFormat, JobStatus


class ContentGenerationJob(BaseModel):
    id: str
    brand_id: str
    status: JobStatus
    content_format: ContentFormat
    user_input: ContentGenerationJobUserInput
    result: ContentGenerationJobResult | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
