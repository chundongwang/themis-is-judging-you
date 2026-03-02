from datetime import datetime, timezone
from sqlalchemy import String, Text, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON
from app.models.base import Base, new_id


class Test(Base):
    __tablename__ = "tests"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    name: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    prompt_template: Mapped[str] = mapped_column(Text, nullable=False)
    scale: Mapped[dict] = mapped_column(JSON, nullable=False)
    population_id: Mapped[str] = mapped_column(
        String, ForeignKey("populations.id"), nullable=False
    )
    panel_size: Mapped[int] = mapped_column(Integer, nullable=False, default=20)
    subjects: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
