from typing import Literal

import public

from aimarketing.domain.campaign_generation.base.model import (
    BaseCampaignGenerationJobUserInput,
    CampaignGenerationJobWorkflowType,
)


@public.add
class AiGeneratedCampaignGenerationJobUserInput(BaseCampaignGenerationJobUserInput):
    workflow_type: Literal[CampaignGenerationJobWorkflowType.AI_GENERATED] = (
        CampaignGenerationJobWorkflowType.AI_GENERATED
    )
