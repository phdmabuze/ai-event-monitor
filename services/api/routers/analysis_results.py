from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from shared.db.tables import AnalysisResult, AnalysisResultMatch

from ..deps import get_session
from ..schemas import AnalysisResultResponse

router = APIRouter(prefix="/analysis-results", tags=["analysis-results"])


@router.get("", response_model=list[AnalysisResultResponse])
async def get_analysis_results(
    session: AsyncSession = Depends(get_session),
    criteria_ids: Annotated[list[int] | None, Query()] = None,
) -> list[AnalysisResult]:
    query = (
        select(AnalysisResult)
        .options(selectinload(AnalysisResult.matches))
        .order_by(AnalysisResult.analyzed_at.desc())
    )

    if criteria_ids is not None:
        query = query.where(
            AnalysisResult.matches.any(
                AnalysisResultMatch.criterion_id.in_(criteria_ids)
            )
        )

    result = await session.execute(query)

    return list(result.scalars().all())
