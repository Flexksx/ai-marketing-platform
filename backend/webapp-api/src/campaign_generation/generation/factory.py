from fastapi import Depends

from src.campaign_generation.generation.ai_generated.service import (
    AIGeneratedCampaignGenerationJobRunner,
)
from src.campaign_generation.generation.product_lifestyle.service import (
    ProductLifestyleCampaignGenerationJobRunner,
)
from src.campaign_generation.generation.shared.service import (
    BaseCampaignGenerationJobRunner,
)
from src.campaign_generation.generation.user_images_only.service import (
    UserImagesOnlyCampaignGenerationJobRunner,
)
from webapp_api_contract.campaign_generation import CampaignGenerationJobWorkflowType


class CampaignGenerationJobRunnerFactory:
    def __init__(
        self,
        user_images_only_runner: UserImagesOnlyCampaignGenerationJobRunner = Depends(),
        ai_generated_runner: AIGeneratedCampaignGenerationJobRunner = Depends(),
        product_lifestyle_runner: ProductLifestyleCampaignGenerationJobRunner = Depends(),
    ):
        self.user_images_only_runner = user_images_only_runner
        self.ai_generated_runner = ai_generated_runner
        self.product_lifestyle_runner = product_lifestyle_runner

    def get_runner(
        self, workflow_type: CampaignGenerationJobWorkflowType
    ) -> BaseCampaignGenerationJobRunner:
        if workflow_type == CampaignGenerationJobWorkflowType.USER_MEDIA_ONLY:
            return self.user_images_only_runner
        if workflow_type == CampaignGenerationJobWorkflowType.AI_GENERATED:
            return self.ai_generated_runner
        if workflow_type == CampaignGenerationJobWorkflowType.PRODUCT_LIFESTYLE:
            return self.product_lifestyle_runner
        raise ValueError(f"No runner found for workflow type: {workflow_type}")
