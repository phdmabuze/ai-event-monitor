from datetime import UTC, datetime

from faststream import AckPolicy
from sqlalchemy import select

from shared.db.session import Session
from shared.db.tables import Criterion
from shared.kafka import Topic, broker
from shared.models.events import AnalysisCompleted, MatchResult, MessageReceived

from .llm import analyze


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
            matches=[],
            analyzed_at=datetime.now(UTC),
        )

    start_time = datetime.now(UTC)
    result = await analyze(message.text, criteria)
    print(
        f"Analysis completed (event_id={message.event_id}) in {(datetime.now(UTC) - start_time).total_seconds():.2f} seconds",
    )

    criteria_by_id = {c.id: c for c in criteria}
    matches = [
        MatchResult(
            criterion_id=match.criterion_id,
            criterion_name=criteria_by_id[match.criterion_id].name,
            criterion_description=criteria_by_id[match.criterion_id].description,
            confidence=match.confidence,
            reason=match.reason,
        )
        for match in result.matches
    ]

    return AnalysisCompleted(
        event_id=message.event_id,
        source=message.source,
        text=message.text,
        matches=matches,
        analyzed_at=datetime.now(UTC),
    )
