from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from shared.db.tables import Criterion, EvalCase, EvalCaseMatch

from ..deps import get_session
from ..schemas import CreateEvalCaseRequest, EvalCaseResponse

router = APIRouter(prefix="/eval-cases", tags=["eval-cases"])


async def _get_eval_case_or_404(session: AsyncSession, eval_case_id: int) -> EvalCase:
    eval_case = await session.get(EvalCase, eval_case_id)
    if eval_case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Eval case not found",
        )
    return eval_case


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=EvalCaseResponse,
)
async def create_eval_case(
    request: CreateEvalCaseRequest,
    session: AsyncSession = Depends(get_session),
) -> EvalCase:
    if request.criterion_ids:
        existing_ids = set(
            (
                await session.execute(
                    select(Criterion.id).where(
                        Criterion.id.in_(request.criterion_ids)
                    )
                )
            )
            .scalars()
            .all()
        )
        missing_ids = set(request.criterion_ids) - existing_ids
        if missing_ids:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Unknown criterion id(s): {sorted(missing_ids)}",
            )

    eval_case = EvalCase(
        text=request.text,
        matches=[
            EvalCaseMatch(criterion_id=criterion_id)
            for criterion_id in request.criterion_ids
        ],
    )
    session.add(eval_case)
    await session.commit()
    return eval_case


@router.get("", response_model=list[EvalCaseResponse])
async def get_eval_cases(
    session: AsyncSession = Depends(get_session),
) -> list[EvalCase]:
    result = await session.execute(
        select(EvalCase)
        .options(selectinload(EvalCase.matches))
        .order_by(EvalCase.id)
    )
    return list(result.scalars().all())


@router.delete("/{eval_case_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_eval_case(
    eval_case_id: int,
    session: AsyncSession = Depends(get_session),
) -> None:
    eval_case = await _get_eval_case_or_404(session, eval_case_id)
    await session.delete(eval_case)
    await session.commit()
