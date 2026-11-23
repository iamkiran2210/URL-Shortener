from datetime import datetime
from uuid import uuid4

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import VARCHAR, UUID, DateTime, func, String

from app.models.base import Base
from app.models.urls import URL


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid4)

    username: Mapped[str] = mapped_column(VARCHAR(60), unique=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    urls: Mapped[list[URL]] = relationship("URL", cascade="all, delete-orphan")
