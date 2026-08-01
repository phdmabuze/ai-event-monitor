from datetime import datetime
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


class AnalysisResultResponse(BaseModel):
    id: int
    event_id: UUID
    source: str
    text: str
    criterion_id: int | None
    criterion_name: str | None
    criterion_description: str | None
    reason: str
    analyzed_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SendMessageRequest(BaseModel):
    source: str
    text: str
