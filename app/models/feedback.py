from datetime import datetime

from sqlalchemy import Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.backend.base import Base


class FeedBack(Base):
    __tablename__ = 'feedback'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id'), nullable=True)
    rating_id: Mapped[int] = mapped_column(Integer, ForeignKey('ratings.id'), nullable=True)
    comment: Mapped[str]
    comment_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)  # Дата отзыва
    is_active: Mapped[bool]

