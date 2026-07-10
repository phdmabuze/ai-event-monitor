from pydantic import BaseModel, Field


class LLMResult(BaseModel):
    matched: bool = Field(
        ...,
        description="Whether the message matches the user's criteria.",
    )
    reason: str = Field(..., description="A short explanation of the decision.")
