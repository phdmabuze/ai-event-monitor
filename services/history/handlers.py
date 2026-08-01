from faststream import AckPolicy
from sqlalchemy.exc import IntegrityError

from shared.db.session import Session
from shared.db.tables import AnalysisResult
from shared.models.events import AnalysisCompleted
from shared.kafka import Topic, broker


@broker.subscriber(
    Topic.ANALYSIS_COMPLETED,
    group_id="history",
    ack_policy=AckPolicy.NACK_ON_ERROR,
)
async def handle(event: AnalysisCompleted) -> None:
    async with Session() as session:
        session.add(AnalysisResult.from_event(event))
        try:
            await session.commit()
        except IntegrityError:
            # event_id already stored - a redelivery of an already-processed
            # message under at-least-once semantics, not a real failure.
            await session.rollback()
