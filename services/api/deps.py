from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from shared.db.session import Session


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with Session() as session:
        yield session
