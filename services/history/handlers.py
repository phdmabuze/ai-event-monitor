from shared.models.events import AnalysisCompleted
from shared.kafka import Topic, broker


@broker.subscriber(Topic.ANALYSIS_COMPLETED)
async def save(result: AnalysisCompleted) -> None:
    print(result.model_dump_json(indent=2))