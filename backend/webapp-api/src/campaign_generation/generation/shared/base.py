from abc import ABC, abstractmethod

from src.campaign_generation.model import (
    CampaignGenerationJob,
    CampaignGenerationJobResult,
)


class BaseCampaignGenerationJobStep(ABC):
    @abstractmethod
    async def execute(self, job: CampaignGenerationJob) -> CampaignGenerationJobResult:
        raise NotImplementedError("execute method must be implemented by subclasses")
