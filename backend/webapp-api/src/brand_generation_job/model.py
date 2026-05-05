from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from lib.model import JobStatus
from lib.scraper.model import ScrapeResult
from src.brand.model import BrandCreateRequest, BrandData


class BrandGenerationJobCreateRequestBody(BaseModel):
    website_url: str = Field(
        ..., description="The URL of the website to extract the brand from"
    )


class BrandGenerationJobCreateRequest(BaseModel):
    website_url: str = Field(
        ..., description="The URL of the website to extract the brand from"
    )
    extra_routes: list[str] = Field(
        default=["/about", "/help"],
        description="The extra routes of the website to extract the brand from",
    )

    model_config = ConfigDict(from_attributes=True)


class BrandGenerationJobAcceptRequest(BaseModel):
    name: str = Field(..., description="The name of the brand")
    data: BrandData


class BrandCreateRequestResponse(BaseModel):
    name: str = Field(...)
    data: BrandData


class BrandGenerationJobResultResponse(BaseModel):
    brand_data: BrandCreateRequestResponse | None = Field(None)
    scraper_result: ScrapeResult | None = Field(None)

    model_config = ConfigDict(from_attributes=True)


class BrandGenerationJobResponse(BaseModel):
    id: str = Field(...)
    status: JobStatus = Field(...)
    result: BrandGenerationJobResultResponse | None = Field(None)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)

    model_config = ConfigDict(from_attributes=True)


class BrandGenerationResult(BaseModel):
    brand_data: BrandCreateRequest | None = Field(None)
    scraper_result: ScrapeResult | None = Field(None)

    model_config = ConfigDict(from_attributes=True)


class BrandGenerationJob(BaseModel):
    id: str = Field(...)
    user_id: str = Field(...)
    status: JobStatus = Field(...)
    website_url: str = Field(...)
    extra_routes: list[str] = Field(default=["/about", "/help"])
    result: BrandGenerationResult | None = Field(None)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)

    model_config = ConfigDict(from_attributes=True)


class BrandGenerationJobUpdateRequest(BaseModel):
    status: JobStatus = Field(..., description="The status of the brand extraction job")
    result: BrandGenerationResult | None = Field(
        None, description="The result of the brand extraction job"
    )

    model_config = ConfigDict(from_attributes=True)
