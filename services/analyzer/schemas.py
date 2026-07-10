from pydantic import BaseModel


class LLMResult(BaseModel):
    matched: bool
    reason: str
