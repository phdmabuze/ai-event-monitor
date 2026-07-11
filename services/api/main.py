from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI

from shared.kafka import broker

from .routers.analysis_results import router as analysis_router
from .routers.messages import router as messages_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await broker.connect()

    yield

    await broker.stop()


app = FastAPI(lifespan=lifespan)

api_router = APIRouter(prefix="/api")
api_router.include_router(messages_router)
api_router.include_router(analysis_router)
app.include_router(api_router)
