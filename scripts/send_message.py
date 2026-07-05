from datetime import UTC, datetime
from uuid import uuid4

from shared.models.events import MessageReceived
from shared.kafka import Topic, broker


async def main() -> None:
    await broker.start()

    try:
        await broker.publish(
            MessageReceived(
                event_id=uuid4(),
                source="manual",
                text="Hello from Kafka!",
                occurred_at=datetime.now(UTC),
            ),
            topic=Topic.MESSAGES_RECEIVED,
        )
    finally:
        await broker.stop()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())