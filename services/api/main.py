from contextlib import asynccontextmanager

from fastapi import FastAPI

from shared.kafka import broker

from .routers.analysis_results import router as analysis_router
from .routers.messages import router as messages_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await broker.connect()

    yield

    await broker.stop()


app = FastAPI(lifespan=lifespan)

app.include_router(messages_router)
app.include_router(analysis_router)
