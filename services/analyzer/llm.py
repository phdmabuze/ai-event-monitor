from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from shared.config import settings

from .criteria import CRITERIA
from .prompts import ANALYSIS_PROMPT, SYSTEM_PROMPT
from .schemas import LLMResult

model = OpenAIChatModel(
    model_name=settings.ollama_model,
    provider=OpenAIProvider(
        base_url=f"{settings.ollama_url}/v1",
        api_key="ollama",
    ),
)


agent = Agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    output_type=LLMResult,
)


async def analyze(text: str) -> LLMResult:
    result = await agent.run(
        ANALYSIS_PROMPT.format(
            criteria=CRITERIA,
            text=text,
        )
    )
    return result.output
