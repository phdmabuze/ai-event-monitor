from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.db.tables import Criterion

from ..deps import get_session
from ..schemas import CreateCriterionRequest, CriterionResponse, UpdateCriterionRequest

router = APIRouter(prefix="/criteria", tags=["criteria"])


async def _get_criterion_or_404(session: AsyncSession, criterion_id: int) -> Criterion:
    criterion = await session.get(Criterion, criterion_id)
    if criterion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Criterion not found",
        )
    return criterion


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=CriterionResponse,
)
async def create_criterion(
    request: CreateCriterionRequest,
    session: AsyncSession = Depends(get_session),
) -> Criterion:
    criterion = Criterion(name=request.name, description=request.description)
    session.add(criterion)
    await session.commit()
    return criterion


@router.get("", response_model=list[CriterionResponse])
async def get_criteria(
    session: AsyncSession = Depends(get_session),
) -> list[Criterion]:
    result = await session.execute(select(Criterion).order_by(Criterion.id))
    return list(result.scalars().all())


@router.patch("/{criterion_id}", response_model=CriterionResponse)
async def update_criterion(
    criterion_id: int,
    request: UpdateCriterionRequest,
    session: AsyncSession = Depends(get_session),
) -> Criterion:
    criterion = await _get_criterion_or_404(session, criterion_id)

    for field, value in request.model_dump(exclude_unset=True).items():
        setattr(criterion, field, value)

    await session.commit()
    return criterion


@router.delete("/{criterion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_criterion(
    criterion_id: int,
    session: AsyncSession = Depends(get_session),
) -> None:
    criterion = await _get_criterion_or_404(session, criterion_id)
    await session.delete(criterion)
    await session.commit()
