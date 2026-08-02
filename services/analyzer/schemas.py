from typing import Literal

from pydantic import BaseModel, Field


class CriterionMatch(BaseModel):
    criterion_id: int = Field(..., description="The id of the matching criterion.")
    confidence: Literal["high", "low"] = Field(
        ...,
        description=(
            "'high' if the message clearly satisfies the criterion, "
            "'low' if it's a borderline or uncertain fit."
        ),
    )
    reason: str = Field(..., description="A short explanation of the decision.")


class LLMResult(BaseModel):
    matches: list[CriterionMatch] = Field(
        default_factory=list,
        description="Criteria the message matches. Empty if none match.",
    )
