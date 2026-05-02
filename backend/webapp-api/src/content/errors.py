import public
from fastapi import HTTPException, status


@public.add
class ContentNotFoundException(HTTPException):
    def __init__(self, post_id: str):
        self.post_id = post_id
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found",
        )
