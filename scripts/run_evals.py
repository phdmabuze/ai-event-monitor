import asyncio
from dataclasses import dataclass

from pydantic import TypeAdapter
from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import Evaluator, EvaluatorContext
from pydantic_evals.reporting import EvaluationReport
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from services.analyzer.llm import analyze
from shared.db.session import Session
from shared.db.tables import Criterion, EvalCase, EvalRun

REPEAT = 3

REPORT_ADAPTER = TypeAdapter(EvaluationReport[str, list[int], type(None)])


@dataclass
class MatchedCriteriaSet(Evaluator[str, list[int], None]):
    def evaluate(self, ctx: EvaluatorContext[str, list[int], None]) -> bool:
        return sorted(ctx.output) == sorted(ctx.expected_output or [])


async def load_criteria() -> list[Criterion]:
    async with Session() as session:
        result = await session.execute(
            select(Criterion).where(Criterion.is_active.is_(True))
        )
        return list(result.scalars().all())


async def load_dataset() -> Dataset[str, list[int], None]:
    async with Session() as session:
        result = await session.execute(
            select(EvalCase).options(selectinload(EvalCase.matches))
        )
        eval_cases = list(result.scalars().all())

    cases = [
        Case(
            name=f"eval-case-{eval_case.id}",
            inputs=eval_case.text,
            expected_output=[match.criterion_id for match in eval_case.matches],
        )
        for eval_case in eval_cases
    ]
    return Dataset(
        name="criteria-matching",
        cases=cases,
        evaluators=[MatchedCriteriaSet()],
    )


async def load_baseline() -> EvaluationReport[str, list[int], None] | None:
    async with Session() as session:
        result = await session.execute(
            select(EvalRun).order_by(EvalRun.created_at.desc()).limit(1)
        )
        last_run = result.scalar_one_or_none()

    if last_run is None:
        return None
    return REPORT_ADAPTER.validate_python(last_run.report)


async def save_run(report: EvaluationReport[str, list[int], None]) -> None:
    async with Session() as session:
        session.add(EvalRun(report=REPORT_ADAPTER.dump_python(report, mode="json")))
        await session.commit()


async def main() -> None:
    criteria = await load_criteria()
    dataset = await load_dataset()

    if not dataset.cases:
        print("No eval cases found. Add some via POST /api/eval-cases.")
        return

    async def task(text: str) -> list[int]:
        result = await analyze(text, criteria)
        return [match.criterion_id for match in result.matches]

    baseline = await load_baseline()
    report = await dataset.evaluate(task, repeat=REPEAT)
    report.print(
        baseline=baseline,
        include_input=True,
        include_expected_output=True,
        include_output=True,
    )
    await save_run(report)


if __name__ == "__main__":
    asyncio.run(main())
