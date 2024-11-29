from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import mapped_column, Mapped

from app.backend.base import Base


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    username: Mapped[str]
    email: Mapped[str] = mapped_column(String, unique=True)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_supplier: Mapped[bool] = mapped_column(Boolean, default=False)
    is_customer: Mapped[bool] = mapped_column(Boolean, default=True)