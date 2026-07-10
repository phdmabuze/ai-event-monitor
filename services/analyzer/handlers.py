from datetime import UTC, datetime

from shared.kafka import Topic, broker
from shared.models.events import AnalysisCompleted, MessageReceived

from .llm import analyze


@broker.subscriber(Topic.MESSAGES_RECEIVED, group_id="analyzer")
@broker.publisher(Topic.ANALYSIS_COMPLETED)
async def handle_message(message: MessageReceived) -> AnalysisCompleted:
    print(f"Analyzing message (event_id={message.event_id}): {message.text:<50}")

    start_time = datetime.now(UTC)
    result = await analyze(message.text)
    print(
        f"Analysis completed (event_id={message.event_id}) in {(datetime.now(UTC) - start_time).total_seconds():.2f} seconds",
    )

    return AnalysisCompleted(
        event_id=message.event_id,
        source=message.source,
        text=message.text,
        matched=result.matched,
        reason=result.reason,
        analyzed_at=datetime.now(UTC),
    )
