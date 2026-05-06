import public
from fastapi import HTTPException, status


@public.add
class ContentPlanItemNotFoundException(HTTPException):
    def __init__(self, item_id: str):
        self.item_id = item_id
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Content plan item with id {item_id} not found",
        )
