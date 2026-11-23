from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import VARCHAR, TEXT, DateTime, func, ForeignKey, UUID
from datetime import datetime

from app.models.base import Base


class URL(Base):
    __tablename__ = "urls"

    short_code: Mapped[str] = mapped_column(VARCHAR(10), primary_key=True)

    long_url: Mapped[str] = mapped_column(TEXT, unique=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
