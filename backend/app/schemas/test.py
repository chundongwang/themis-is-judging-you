from datetime import datetime
from pydantic import BaseModel
from app.schemas.common import ScaleConfig, Subject


class TestRead(BaseModel):
    id: str
    name: str
    created_at: datetime
    prompt_template: str
    scale: ScaleConfig
    population_id: str
    panel_size: int
    subjects: list[Subject]

    model_config = {"from_attributes": True}


class TestCreate(BaseModel):
    id: str | None = None
    name: str
    prompt_template: str
    scale: ScaleConfig
    population_id: str
    panel_size: int = 20
    subjects: list[Subject] = []


class TestUpdate(BaseModel):
    name: str | None = None
    prompt_template: str | None = None
    scale: ScaleConfig | None = None
    population_id: str | None = None
    panel_size: int | None = None
    subjects: list[Subject] | None = None
