from pydantic import BaseModel


class ReviewRequest(BaseModel):
    product_id: int
    rating: int
    comment: str
