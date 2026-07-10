from datetime import UTC, datetime
from uuid import uuid4

from fastapi import APIRouter, status

from services.api.schemas import SendMessageRequest
from shared.models.events import MessageReceived
from shared.kafka import Topic, broker

router = APIRouter(
    prefix="/messages",
    tags=["messages"],
)


@router.post(
    "",
    status_code=status.HTTP_202_ACCEPTED,
)
async def send_message(
    request: SendMessageRequest,
) -> None:
    message = MessageReceived(
        event_id=uuid4(),
        source=request.source,
        text=request.text,
        occurred_at=datetime.now(UTC),
    )

    await broker.publish(
        message,
        topic=Topic.MESSAGES_RECEIVED,
    )
