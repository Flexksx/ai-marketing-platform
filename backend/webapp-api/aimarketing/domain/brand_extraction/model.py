from datetime import datetime

import public
from pydantic import BaseModel, ConfigDict, Field

from aimarketing.domain.brand.schema import BrandCreateRequest
from aimarketing.lib.job.model import JobStatus
from aimarketing.lib.scraper.model import ScrapeResult


@public.add
class BrandGenerationResult(BaseModel):
    brand_data: BrandCreateRequest | None = Field(
        None,
    )
    scraper_result: ScrapeResult | None = Field(
        None,
    )

    model_config = ConfigDict(from_attributes=True)


@public.add
class BrandGenerationJob(BaseModel):
    id: str = Field(
        ...,
    )
    user_id: str = Field(
        ...,
    )
    status: JobStatus = Field(
        ...,
    )
    website_url: str = Field(
        ...,
    )
    extra_routes: list[str] = Field(
        default=["/about", "/help"],
    )
    result: BrandGenerationResult | None = Field(
        None,
    )
    created_at: datetime = Field(
        ...,
    )
    updated_at: datetime = Field(
        ...,
    )
    model_config = ConfigDict(from_attributes=True)
