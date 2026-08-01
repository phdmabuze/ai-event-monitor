from datetime import UTC, datetime

from faststream import AckPolicy
from sqlalchemy import select

from shared.db.session import Session
from shared.db.tables import Criterion
from shared.kafka import Topic, broker
from shared.models.events import AnalysisCompleted, MessageReceived

from .llm import analyze

NO_ACTIVE_CRITERIA_REASON = "No active criteria to evaluate against."


@broker.subscriber(
    Topic.MESSAGES_RECEIVED,
    group_id="analyzer",
    ack_policy=AckPolicy.REJECT_ON_ERROR,
)
@broker.publisher(Topic.ANALYSIS_COMPLETED)
async def handle_message(message: MessageReceived) -> AnalysisCompleted:
    print(f"Analyzing message (event_id={message.event_id}): {message.text:<50}")

    async with Session() as session:
        criteria_result = await session.execute(
            select(Criterion).where(Criterion.is_active.is_(True))
        )
        criteria = list(criteria_result.scalars().all())

    if not criteria:
        return AnalysisCompleted(
            event_id=message.event_id,
            source=message.source,
            text=message.text,
            criterion_id=None,
            criterion_name=None,
            criterion_description=None,
            reason=NO_ACTIVE_CRITERIA_REASON,
            analyzed_at=datetime.now(UTC),
        )

    start_time = datetime.now(UTC)
    result = await analyze(message.text, criteria)
    print(
        f"Analysis completed (event_id={message.event_id}) in {(datetime.now(UTC) - start_time).total_seconds():.2f} seconds",
    )

    matched_criterion = next(
        (c for c in criteria if c.id == result.criterion_id), None
    )

    return AnalysisCompleted(
        event_id=message.event_id,
        source=message.source,
        text=message.text,
        criterion_id=matched_criterion.id if matched_criterion else None,
        criterion_name=matched_criterion.name if matched_criterion else None,
        criterion_description=(
            matched_criterion.description if matched_criterion else None
        ),
        reason=result.reason,
        analyzed_at=datetime.now(UTC),
    )
