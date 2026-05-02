from datetime import datetime

import public
from pydantic import BaseModel, ConfigDict, Field

from webapp_api_contract.brands import BrandData
from webapp_api_contract.brand_extraction import (
    BrandGenerationResult,
)
from webapp_api_contract.shared import JobStatus
from scraper_api_contract.scraper import ScrapeResult


@public.add
class BrandGenerationJobCreateRequestBody(BaseModel):
    website_url: str = Field(
        ..., description="The URL of the website to extract the brand from"
    )


@public.add
class BrandGenerationJobCreateRequest(BaseModel):
    website_url: str = Field(
        ..., description="The URL of the website to extract the brand from"
    )
    extra_routes: list[str] = Field(
        default=["/about", "/help"],
        description="The extra routes of the website to extract the brand from",
    )
    model_config = ConfigDict(from_attributes=True)


@public.add
class BrandGenerationJobUpdateRequest(BaseModel):
    status: JobStatus = Field(..., description="The status of the brand extraction job")
    result: BrandGenerationResult | None = Field(
        None, description="The result of the brand extraction job"
    )
    model_config = ConfigDict(from_attributes=True)


@public.add
class BrandGenerationJobAcceptRequest(BaseModel):
    name: str = Field(..., description="The name of the brand")
    data: BrandData


@public.add
class BrandCreateRequestResponse(BaseModel):
    name: str = Field(
        ...,
    )
    data: BrandData


@public.add
class BrandGenerationJobResultResponse(BaseModel):
    brand_data: BrandCreateRequestResponse | None = Field(
        None,
    )
    scraper_result: ScrapeResult | None = Field(
        None,
    )
    model_config = ConfigDict(from_attributes=True)


@public.add
class BrandGenerationJobResponse(BaseModel):
    id: str = Field(
        ...,
    )
    status: JobStatus = Field(
        ...,
    )
    result: BrandGenerationJobResultResponse | None = Field(
        None,
    )
    created_at: datetime = Field(
        ...,
    )
    updated_at: datetime = Field(
        ...,
    )
    model_config = ConfigDict(from_attributes=True)
