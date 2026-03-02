from datetime import datetime, timezone
from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON
from app.models.base import Base, new_id


class Run(Base):
    __tablename__ = "runs"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    test_id: Mapped[str] = mapped_column(
        String, ForeignKey("tests.id"), nullable=False
    )
    executed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    panel_size: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    status: Mapped[str] = mapped_column(String, nullable=False, default="pending")
    results: Mapped[list] = mapped_column(JSON, nullable=True, default=None)
    log_id: Mapped[str | None] = mapped_column(String, nullable=True, default=None)
