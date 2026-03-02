from pydantic import BaseModel
from app.schemas.common import DimensionConfig


class PopulationRead(BaseModel):
    id: str
    name: str
    description: str
    dimensions: list[DimensionConfig]

    model_config = {"from_attributes": True}


class PopulationCreate(BaseModel):
    id: str | None = None
    name: str
    description: str = ""
    dimensions: list[DimensionConfig] = []


class PopulationUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    dimensions: list[DimensionConfig] | None = None
