import asyncio

from aiokafka.admin import AIOKafkaAdminClient, NewTopic

from shared.config import settings
from shared.kafka import Topic


TOPICS = (
    NewTopic(
        name=Topic.MESSAGES_RECEIVED,
        num_partitions=1,
        replication_factor=1,
    ),
    NewTopic(
        name=Topic.ANALYSIS_COMPLETED,
        num_partitions=1,
        replication_factor=1,
    ),
)


async def main() -> None:
    admin = AIOKafkaAdminClient(
        bootstrap_servers=settings.kafka_bootstrap_servers,
    )

    await admin.start()

    try:
        existing_topics = await admin.list_topics()

        topics_to_create = [
            topic for topic in TOPICS if topic.name not in existing_topics
        ]

        if not topics_to_create:
            print("All topics already exist.")
            return

        await admin.create_topics(topics_to_create)

        print(
            "Created topics:",
            ", ".join(topic.name for topic in topics_to_create),
        )

    finally:
        await admin.close()


if __name__ == "__main__":
    asyncio.run(main())
