from contextlib import asynccontextmanager

from fastapi import FastAPI

from services.api.routers.analysis_results import router as analysis_router
from services.api.routers.messages import router as messages_router
from shared.kafka import broker


@asynccontextmanager
async def lifespan(app: FastAPI):
    await broker.connect()

    yield

    await broker.stop()


app = FastAPI(lifespan=lifespan)

app.include_router(messages_router)
app.include_router(analysis_router)