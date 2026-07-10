from datetime import UTC, datetime
from shared.kafka import broker, Topic
from shared.models.events import AnalysisCompleted, MessageReceived


@broker.subscriber(Topic.MESSAGES_RECEIVED, group_id="analyzer")
@broker.publisher(Topic.ANALYSIS_COMPLETED)
async def analyze(message: MessageReceived) -> AnalysisCompleted:
    print(f"Analyzing message: {message.text}")

    return AnalysisCompleted(
        event_id=message.event_id,
        source=message.source,
        text=message.text,
        matched=True,
        reason="Stub",
        analyzed_at=datetime.now(UTC),
    )
