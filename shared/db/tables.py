from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from shared.db import Base


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), unique=True)
    source: Mapped[str] = mapped_column(String(64))
    text: Mapped[str] = mapped_column(Text)
    matched: Mapped[bool]
    reason: Mapped[str] = mapped_column(Text)
    analyzed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))