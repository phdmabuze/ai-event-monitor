from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from shared.config import settings


engine: AsyncEngine = create_async_engine(
    settings.postgres_url,
    echo=False,
)
