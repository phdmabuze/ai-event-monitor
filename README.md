# AI Event Monitor
AI Event Monitor is an event-driven system for filtering incoming messages using an LLM. It can be used to automatically detect messages matching user-defined criteria (for example, Python backend job opportunities) from external sources such as Telegram channels or other message streams.

*This project was created to demonstrate modern backend architecture patterns, asynchronous processing, and local LLM integration.*

## Features

- Receive messages through a REST API
- Asynchronously process messages using Kafka
- Classify messages with an LLM, provider configurable via `.env` (Anthropic, OpenAI, or any self-hosted OpenAI-compatible endpoint such as Ollama)
- Store analysis results in PostgreSQL
- Browse results through REST API
- Fully containerized deployment

## Components

- **API** — receives incoming messages and exposes REST endpoints for results.
- **Analyzer** — evaluates messages using the configured criteria and the configured LLM provider.
- **History** — stores completed analysis results in PostgreSQL.
- **Kafka** — provides asynchronous communication between services.

## How It Works

1. Filtering criteria are managed through the REST API (`POST/GET/PATCH/DELETE /api/criteria`) and stored in PostgreSQL — each criterion has a `name` and `description`, and can be deactivated (`is_active=false`) without deleting past results tied to it. Example:

```json
{"name": "Python backend", "description": "Jobs, freelance, FastAPI/Django/PostgreSQL, remote work."}
```

2. External services send messages from different sources through a unified REST API endpoint (`POST /api/messages`). The API publishes incoming messages to Kafka for asynchronous processing.

3. The **Analyzer service** consumes messages from Kafka, loads the currently active criteria from PostgreSQL, and asks the LLM which criteria (zero, one, or several) the message matches, each with a `confidence` of `"high"` or `"low"`.

4. Analysis results are published back to Kafka. The **History service** consumes completed analysis events and stores them in PostgreSQL, along with a snapshot of each matched criterion's name/description at the time of the match (so later edits or deletions of a criterion don't rewrite history).

5. Users can retrieve processed messages and their analysis results through the REST API endpoint (`GET /api/analysis-results`, optionally filtered by `criteria_ids`):
```json
[
  {
    "source": "telegram",
    "text": "Hiring: Python Backend Developer (FastAPI, PostgreSQL). Remote position. Experience with async Python required.",
    "matches": [
      {
        "criterion_id": 1,
        "criterion_name": "Python backend",
        "criterion_description": "Jobs, freelance, FastAPI/Django/PostgreSQL, remote work.",
        "confidence": "high",
        "reason": "The message describes a remote Python developer position requiring FastAPI and PostgreSQL experience."
      }
    ]
  },
  {
    "source": "telegram",
    "text": "Looking for a Frontend Developer to join our team. Strong experience with React, TypeScript, and modern UI development is required.",
    "matches": []
  }
]
```

## Evals

Because the Analyzer sends every active criterion to the LLM in a single call, editing one criterion's wording can silently change how messages are classified against *other* criteria too. Evals are a regression check against that: a growing set of human-confirmed examples (message + the criteria it should match) that gets replayed against the current criteria/prompt whenever something changes.

Add an example through `POST /api/eval-cases` — `criterion_ids` is the set of criteria the message is expected to match (empty list if it should match none):

```json
{"text": "Hiring: Python Backend Developer (FastAPI, PostgreSQL). Remote position.", "criterion_ids": [1]}
```

Existing cases can be listed (`GET /api/eval-cases`) or removed (`DELETE /api/eval-cases/{id}`) — e.g. once a case's expectation no longer matches an intentional change to a criterion.

Run the eval suite with:
```bash
uv run python -m scripts.run_evals
```
This replays every stored case through the current criteria and LLM (each case 3 times, to smooth out LLM sampling noise), then prints a report comparing the result to the previous run — not just pass/fail for this run, but what got better or worse since the last time you ran it. Each run's report is saved to PostgreSQL so the next run has something to diff against.

## Tech Stack

Python 3.13 • FastAPI • FastStream • Apache Kafka • PostgreSQL • SQLAlchemy • Alembic • PydanticAI • pydantic-evals • Docker Compose

## Quick Start

```bash
cp .env.example .env
```
Set `LLM_PROVIDER`, `LLM_MODEL`, and the matching API key (e.g. `ANTHROPIC_API_KEY`) in `.env`.
To use a self-hosted OpenAI-compatible endpoint instead (e.g. a local Ollama instance running outside this compose setup), set `LLM_BASE_URL` instead of a hosted provider's API key.

```bash
docker compose up
```
Swagger UI will be available at http://localhost:8000/docs

