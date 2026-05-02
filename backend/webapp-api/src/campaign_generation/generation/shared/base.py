from abc import ABC, abstractmethod

from webapp_api_contract.campaign_generation import (
    CampaignGenerationJob,
    CampaignGenerationJobResult,
)


class BaseCampaignGenerationJobStep(ABC):
    @abstractmethod
    async def execute(self, job: CampaignGenerationJob) -> CampaignGenerationJobResult:
        raise NotImplementedError("execute method must be implemented by subclasses")
