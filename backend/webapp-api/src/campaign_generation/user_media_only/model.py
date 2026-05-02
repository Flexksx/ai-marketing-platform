from typing import Literal

import public

from webapp_api_contract.campaign_generation import (
    BaseCampaignGenerationJobUserInput,
    CampaignGenerationJobWorkflowType,
)


@public.add
class UserMediaOnlyCampaignGenerationJobUserInput(BaseCampaignGenerationJobUserInput):
    workflow_type: Literal[CampaignGenerationJobWorkflowType.USER_MEDIA_ONLY] = (
        CampaignGenerationJobWorkflowType.USER_MEDIA_ONLY
    )
    image_urls: list[str]
