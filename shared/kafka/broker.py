from faststream.kafka import KafkaBroker

from shared.config import settings


broker = KafkaBroker(
    bootstrap_servers=settings.kafka_bootstrap_servers,
)