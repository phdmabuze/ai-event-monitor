from datetime import datetime
from uuid import UUID
from typing import Any
from pydantic import BaseModel, Field


class MessageReceived(BaseModel):
    event_id: UUID
    source: str
    text: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    occurred_at: datetime


class AnalysisCompleted(BaseModel):
    event_id: UUID
    source: str
    text: str
    criterion_id: int | None
    criterion_name: str | None
    criterion_description: str | None
    reason: str
    analyzed_at: datetime
