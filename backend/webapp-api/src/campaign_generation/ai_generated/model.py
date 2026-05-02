from typing import Literal

import public

from webapp_api_contract.campaign_generation import (
    BaseCampaignGenerationJobUserInput,
    CampaignGenerationJobWorkflowType,
)


@public.add
class AiGeneratedCampaignGenerationJobUserInput(BaseCampaignGenerationJobUserInput):
    workflow_type: Literal[CampaignGenerationJobWorkflowType.AI_GENERATED] = (
        CampaignGenerationJobWorkflowType.AI_GENERATED
    )
