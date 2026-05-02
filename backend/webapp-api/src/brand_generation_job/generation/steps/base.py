from abc import ABC, abstractmethod

from src.brand_generation_job.model import BrandGenerationJob, BrandGenerationResult


class BrandGenerationBaseStep(ABC):
    @abstractmethod
    async def execute(self, job: BrandGenerationJob) -> BrandGenerationResult:
        raise NotImplementedError("execute method must be implemented by subclasses")
