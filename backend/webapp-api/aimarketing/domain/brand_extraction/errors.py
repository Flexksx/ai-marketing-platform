import public
from fastapi import HTTPException, status


@public.add
class BrandGenerationJobNotFoundError(HTTPException):
    def __init__(self, job_id: str):
        self.job_id = job_id
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Brand generation job with id {job_id} not found",
        )


@public.add
class BrandGenerationJobResultElementNotFoundError(HTTPException):
    def __init__(self, job_id: str, element_name: str):
        self.job_id = job_id
        self.element_name = element_name
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Brand generation job result element {element_name} with id {job_id} not found",
        )


@public.add
class BrandGenerationJobResultNotFoundError(HTTPException):
    def __init__(self, job_id: str):
        self.job_id = job_id
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Brand generation job with id {job_id} does not have a result",
        )
