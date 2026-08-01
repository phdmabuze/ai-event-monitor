from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from shared.db import Base
from shared.models.events import AnalysisCompleted


class Criterion(Base):
    __tablename__ = "criteria"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), unique=True)
    source: Mapped[str] = mapped_column(String(64))
    text: Mapped[str] = mapped_column(Text)
    criterion_id: Mapped[int | None] = mapped_column(
        ForeignKey("criteria.id", ondelete="CASCADE")
    )
    criterion_name: Mapped[str | None] = mapped_column(String(128))
    criterion_description: Mapped[str | None] = mapped_column(Text)
    reason: Mapped[str] = mapped_column(Text)
    analyzed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    @classmethod
    def from_event(cls, event: AnalysisCompleted) -> "AnalysisResult":
        return cls(
            event_id=event.event_id,
            source=event.source,
            text=event.text,
            criterion_id=event.criterion_id,
            criterion_name=event.criterion_name,
            criterion_description=event.criterion_description,
            reason=event.reason,
            analyzed_at=event.analyzed_at,
        )
