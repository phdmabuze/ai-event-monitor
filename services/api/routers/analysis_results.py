from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.deps import get_session
from services.api.schemas import AnalysisResultResponse
from shared.db.tables import AnalysisResult

router = APIRouter(prefix="/analysis-results", tags=["analysis-results"])


@router.get("", response_model=list[AnalysisResultResponse])
async def get_analysis_results(
    session: AsyncSession = Depends(get_session),
    matched: Annotated[bool | None, Query()] = None,
) -> list[AnalysisResult]:
    query = select(AnalysisResult)

    if matched is not None:
        query = query.where(AnalysisResult.matched == matched)

    result = await session.execute(query)

    return list(result.scalars().all())
