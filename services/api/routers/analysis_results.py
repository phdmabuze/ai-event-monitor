from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.db.tables import AnalysisResult

from ..deps import get_session
from ..schemas import AnalysisResultResponse

router = APIRouter(prefix="/analysis-results", tags=["analysis-results"])


@router.get("", response_model=list[AnalysisResultResponse])
async def get_analysis_results(
    session: AsyncSession = Depends(get_session),
    criteria_ids: Annotated[list[int] | None, Query()] = None,
) -> list[AnalysisResult]:
    query = select(AnalysisResult).order_by(AnalysisResult.analyzed_at.desc())

    if criteria_ids is not None:
        query = query.where(AnalysisResult.criterion_id.in_(criteria_ids))

    result = await session.execute(query)

    return list(result.scalars().all())
