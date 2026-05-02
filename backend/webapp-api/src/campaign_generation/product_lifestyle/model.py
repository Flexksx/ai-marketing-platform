from typing import Literal

import public
from pydantic import Field

from webapp_api_contract.campaign_generation import (
    BaseCampaignGenerationJobUserInput,
    CampaignGenerationJobWorkflowType,
)


@public.add
class ProductLifestyleCampaignGenerationJobUserInput(
    BaseCampaignGenerationJobUserInput
):
    workflow_type: Literal[CampaignGenerationJobWorkflowType.PRODUCT_LIFESTYLE] = (
        CampaignGenerationJobWorkflowType.PRODUCT_LIFESTYLE
    )
    image_urls: list[str] = Field(
        ...,
        description="List of product image URLs to be preserved in generated lifestyle images",
    )
