from __future__ import annotations

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON
from app.models.base import Base, new_id


class RunLog(Base):
    __tablename__ = "run_logs"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    run_id: Mapped[str] = mapped_column(
        String, ForeignKey("runs.id"), nullable=False
    )
    entries: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
