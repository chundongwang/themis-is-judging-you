from datetime import datetime
from pydantic import BaseModel
from app.schemas.common import SubjectResult


class RunRead(BaseModel):
    id: str
    test_id: str
    executed_at: datetime
    panel_size: int
    status: str
    results: list[SubjectResult] | None = None
    log_id: str | None = None

    model_config = {"from_attributes": True}


class RunCreate(BaseModel):
    test_id: str


class SSEProgressEvent(BaseModel):
    completed: int
    total: int
    pct: float


class SSEJudgeResultEvent(BaseModel):
    judge: dict
    score: float
    reason: str


class SSECompleteEvent(BaseModel):
    mean: float
    median: float
    std: float
    histogram: list[dict]
