from fastapi import HTTPException, status


class CampaignGenerationJobProcessingFailureException(HTTPException):
    def __init__(self, job_id: str, error: Exception):
        self.job_id = job_id
        self.error = error
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process campaign generation job {job_id}: {error}",
        )


class CampaignGenerationJobGenerationFailureException(HTTPException):
    def __init__(self, job_id: str, message: str):
        self.job_id = job_id
        self.message = message
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate campaign data for job {job_id}: {message}",
        )
