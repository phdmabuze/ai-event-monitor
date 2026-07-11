# AI Event Monitor
AI Event Monitor is an event-driven system for filtering incoming messages using a local LLM. It can be used to automatically detect messages matching user-defined criteria (for example, Python backend job opportunities) from external sources such as Telegram channels or other message streams.

*This project was created to demonstrate modern backend architecture patterns, asynchronous processing, and local LLM integration.*

## Features

- Receive messages through a REST API
- Asynchronously process messages using Kafka
- Classify messages with a local LLM
- Store analysis results in PostgreSQL
- Browse results through REST API
- Fully containerized deployment

## Components

- **API** — receives incoming messages and exposes REST endpoints for results.
- **Analyzer** — evaluates messages using the configured criteria and local LLM.
- **History** — stores completed analysis results in PostgreSQL.
- **Kafka** — provides asynchronous communication between services.
- **Ollama** — runs the local LLM used for classification.

## How It Works

1. A filtering criterion is configured for incoming messages (currently defined in `services/analyzer/criteria.py`):

```text
Match messages related to:

- Python backend: jobs, freelance, FastAPI/Django/PostgreSQL, remote work.
- Open source: Python projects and collaboration opportunities.
- TON ecosystem: TON, DeFi, blockchain projects and news.
```

2. External services send messages from different sources through a unified REST API endpoint (`POST /api/messages`). The API publishes incoming messages to Kafka for asynchronous processing.

3. The **Analyzer service** consumes messages from Kafka and evaluates them against the configured criteria using a local LLM.

4. Analysis results are published back to Kafka. The **History service** consumes completed analysis events and stores them in PostgreSQL.

5. Users can retrieve processed messages and their analysis results through the REST API endpoint (`GET /api/analysis-results`):
```json
[
  {
    "source": "telegram",
    "text": "Hiring: Python Backend Developer (FastAPI, PostgreSQL). Remote position. Experience with async Python required.",
    "matched": true,
    "reason": "The message matches the Python backend criteria as it describes a remote Python developer position requiring FastAPI and PostgreSQL experience."
  },
  {
    "source": "telegram",
    "text": "Looking for a Frontend Developer to join our team. Strong experience with React, TypeScript, and modern UI development is required.",
    "matched": false,
    "reason": "The message is related to frontend development and does not match the configured criteria for Python backend jobs, open source projects, or TON ecosystem opportunities."
  }
]
```

## Tech Stack

Python 3.13 • FastAPI • FastStream • Apache Kafka • PostgreSQL • SQLAlchemy • Alembic • PydanticAI • Ollama • Docker Compose

## Quick Start

```bash
cp .env.example .env
docker compose up
```
Swagger UI will be available at http://localhost:8000/docs

