from abc import ABC, abstractmethod

from vozai.domain.campaign_generation.model import (
    CampaignGenerationJob,
    CampaignGenerationJobResult,
)


class BaseCampaignGenerationJobStep(ABC):
    @abstractmethod
    async def execute(self, job: CampaignGenerationJob) -> CampaignGenerationJobResult:
        raise NotImplementedError("execute method must be implemented by subclasses")
