from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from shared.config import settings

from .criteria import CRITERIA
from .prompts import ANALYSIS_PROMPT, SYSTEM_PROMPT
from .schemas import LLMResult

if settings.llm_base_url:
    # Self-hosted OpenAI-compatible endpoint (e.g. Ollama, LM Studio).
    model = OpenAIChatModel(
        model_name=settings.llm_model,
        provider=OpenAIProvider(
            base_url=settings.llm_base_url,
            api_key=settings.llm_api_key or "not-needed",
        ),
    )
else:
    # Hosted provider (openai, anthropic, ...); API key is read from its
    # standard env var (OPENAI_API_KEY, ANTHROPIC_API_KEY, ...).
    model = f"{settings.llm_provider}:{settings.llm_model}"


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
