from pydantic import BaseModel, Field


class LLMResult(BaseModel):
    criterion_id: int | None = Field(
        ...,
        description="The id of the matching criterion, or null if none match.",
    )
    reason: str = Field(..., description="A short explanation of the decision.")
