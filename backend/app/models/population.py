from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON
from app.models.base import Base, new_id


class Population(Base):
    __tablename__ = "populations"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    dimensions: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
