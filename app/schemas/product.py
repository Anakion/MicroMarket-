from pydantic import BaseModel


class CreateProduct(BaseModel):
    name: str
    description: str
    price: int
    image_url: str
    stock: int
    rating: float
    category: int
