from shared.db.session import Session
from shared.db.tables import AnalysisResult
from shared.models.events import AnalysisCompleted
from shared.kafka import Topic, broker


@broker.subscriber(Topic.ANALYSIS_COMPLETED, group_id="history")
async def handle(event: AnalysisCompleted) -> None:
    async with Session() as session:
        session.add(AnalysisResult.from_event(event))
        await session.commit()