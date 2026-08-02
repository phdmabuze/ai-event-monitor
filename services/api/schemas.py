from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CriterionResponse(BaseModel):
    id: int
    name: str
    description: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CreateCriterionRequest(BaseModel):
    name: str
    description: str


class UpdateCriterionRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class MatchResponse(BaseModel):
    criterion_id: int
    criterion_name: str
    criterion_description: str
    confidence: Literal["high", "low"]
    reason: str

    model_config = ConfigDict(from_attributes=True)


class AnalysisResultResponse(BaseModel):
    id: int
    event_id: UUID
    source: str
    text: str
    matches: list[MatchResponse]
    analyzed_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SendMessageRequest(BaseModel):
    source: str
    text: str
