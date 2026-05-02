import public
from fastapi import HTTPException, status


@public.add
class BrandNotFoundError(HTTPException):
    def __init__(self, brand_id: str):
        self.brand_id = brand_id
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Brand with id {brand_id} not found",
        )
