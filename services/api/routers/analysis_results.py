from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.deps import get_session
from services.api.schemas import AnalysisResultResponse
from shared.db.tables import AnalysisResult

router = APIRouter(prefix="/analysis-results", tags=["analysis-results"])


@router.get("", response_model=list[AnalysisResultResponse])
async def get_analysis_results(
    session: AsyncSession = Depends(get_session),
) -> list[AnalysisResult]:
    result = await session.execute(
        select(AnalysisResult).order_by(
            AnalysisResult.analyzed_at.desc()
        )
    )

    return list(result.scalars())