from typing import Literal, Union, Annotated
from pydantic import BaseModel, Field


class WeightEntry(BaseModel):
    value: str
    weight: float


class ContinuousDistribution(BaseModel):
    fn: Literal["normal", "skewed_normal", "uniform"]
    mu: float
    sigma: float
    min: float
    max: float


class CategoricalDistribution(BaseModel):
    fn: Literal["weighted"]
    weights: list[WeightEntry]


Distribution = Annotated[
    Union[ContinuousDistribution, CategoricalDistribution],
    Field(discriminator="fn"),
]


class DimensionConfig(BaseModel):
    name: str
    type: Literal["continuous", "categorical"]
    distribution: ContinuousDistribution | CategoricalDistribution

    model_config = {"from_attributes": True}


class ScaleConfig(BaseModel):
    min: float
    max: float
    label: str

    model_config = {"from_attributes": True}


class Subject(BaseModel):
    id: str
    text: str
    image: str | None = None

    model_config = {"from_attributes": True}


class SubjectResult(BaseModel):
    subject_id: str
    mean: float
    median: float
    std: float
    histogram: list[dict]

    model_config = {"from_attributes": True}
