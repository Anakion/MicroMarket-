from app.backend.base import Base
from sqlalchemy import ForeignKey, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship, mapped_column, Mapped


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str]
    slug: Mapped[str] = mapped_column(String, unique=True, index=True)
    description: Mapped[str]
    price: Mapped[int]
    image_url: Mapped[str]
    stock: Mapped[int]
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id', ondelete='CASCADE'))
    rating: Mapped[float]
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    category = relationship('Category', back_populates='products')