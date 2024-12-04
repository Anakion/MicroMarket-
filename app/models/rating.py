from sqlalchemy import Integer, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from app.backend.base import Base


class Rating(Base):
    __tablename__ = 'rating'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    grade: Mapped[int]
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id'))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)



