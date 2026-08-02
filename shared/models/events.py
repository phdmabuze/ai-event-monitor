from datetime import datetime
from uuid import UUID
from typing import Any, Literal
from pydantic import BaseModel, Field


class MessageReceived(BaseModel):
    event_id: UUID
    source: str
    text: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    occurred_at: datetime


class MatchResult(BaseModel):
    criterion_id: int
    criterion_name: str
    criterion_description: str
    confidence: Literal["high", "low"]
    reason: str


class AnalysisCompleted(BaseModel):
    event_id: UUID
    source: str
    text: str
    matches: list[MatchResult]
    analyzed_at: datetime
