from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from scraper_api_contract.scraper import ScrapeResult

from webapp_api_contract.brand import BrandData
from webapp_api_contract.shared import JobStatus


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
