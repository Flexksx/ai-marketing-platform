from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from webapp_api_contract.content_generation.model import (
    ContentGenerationJobResult,
    ContentGenerationJobUserInput,
)
from webapp_api_contract.shared import ContentFormat, JobStatus


class ContentGenerationJobCreateRequest(BaseModel):
    brand_id: str = Field(..., description="The ID of the brand for the content")
    user_input: ContentGenerationJobUserInput
    content_format: ContentFormat

    model_config = ConfigDict(from_attributes=True)


class ContentGenerationJobUpdateRequest(BaseModel):
    status: JobStatus | None = Field(None)
    result: ContentGenerationJobResult | None = Field(None)


class ContentGenerationJobSearchRequest(BaseModel):
    brand_id: str | None = None


class ContentGenerationJobResponse(BaseModel):
    id: str
    brand_id: str
    status: JobStatus
    content_format: ContentFormat
    user_input: ContentGenerationJobUserInput
    result: ContentGenerationJobResult | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
