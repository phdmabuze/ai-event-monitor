from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AnalysisResultResponse(BaseModel):
    id: int
    event_id: UUID
    source: str
    text: str
    matched: bool
    reason: str
    analyzed_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SendMessageRequest(BaseModel):
    source: str
    text: str
