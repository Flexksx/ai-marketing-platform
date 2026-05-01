from abc import ABC, abstractmethod

from vozai.domain.brand_extraction.model import (
    BrandGenerationJob,
    BrandGenerationResult,
)


class BrandGenerationBaseStep(ABC):
    @abstractmethod
    async def execute(self, job: BrandGenerationJob) -> BrandGenerationResult:
        raise NotImplementedError("execute method must be implemented by subclasses")

