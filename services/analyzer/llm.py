from pydantic_ai import Agent, ModelRetry, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from shared.config import settings
from shared.db.tables import Criterion

from .prompts import ANALYSIS_PROMPT, CRITERION_LINE, SYSTEM_PROMPT
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
    deps_type=frozenset[int],
)


@agent.output_validator
def validate_matches(ctx: RunContext[frozenset[int]], data: LLMResult) -> LLMResult:
    seen: set[int] = set()
    for match in data.matches:
        if match.criterion_id not in ctx.deps:
            raise ModelRetry(
                f"criterion_id must be one of {sorted(ctx.deps)}, "
                f"got {match.criterion_id}"
            )
        if match.criterion_id in seen:
            raise ModelRetry(
                f"criterion_id {match.criterion_id} was returned more than once"
            )
        seen.add(match.criterion_id)
    return data


async def analyze(text: str, criteria: list[Criterion]) -> LLMResult:
    criteria_block = "\n".join(
        CRITERION_LINE.format(id=c.id, name=c.name, description=c.description)
        for c in criteria
    )
    result = await agent.run(
        ANALYSIS_PROMPT.format(criteria=criteria_block, text=text),
        deps=frozenset(c.id for c in criteria),
    )
    return result.output
