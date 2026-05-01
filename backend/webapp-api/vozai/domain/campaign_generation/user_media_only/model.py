from typing import Literal

import public

from vozai.domain.campaign_generation.base.model import (
    BaseCampaignGenerationJobUserInput,
    CampaignGenerationJobWorkflowType,
)


@public.add
class UserMediaOnlyCampaignGenerationJobUserInput(BaseCampaignGenerationJobUserInput):
    workflow_type: Literal[CampaignGenerationJobWorkflowType.USER_MEDIA_ONLY] = (
        CampaignGenerationJobWorkflowType.USER_MEDIA_ONLY
    )
    image_urls: list[str]
