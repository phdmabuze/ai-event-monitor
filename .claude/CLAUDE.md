# AI Event Monitor

Event-driven system that filters incoming messages (e.g. Telegram) using a local LLM, based on user-defined criteria.

## Architecture

- **services/api** — FastAPI app, receives messages via `POST /api/messages`, publishes to Kafka; exposes `GET /api/analysis-results`.
- **services/analyzer** — Kafka consumer, evaluates messages against criteria (`services/analyzer/criteria.py`) using a local LLM via PydanticAI + Ollama, publishes results back to Kafka.
- **services/history** — Kafka consumer, persists completed analysis results to PostgreSQL.
- **shared/** — code shared across services: `config.py`, `db/`, `kafka/`, `models/`.

Tech: Python 3.13, FastAPI, FastStream, Kafka, PostgreSQL, SQLAlchemy, Alembic, PydanticAI, Ollama, Docker Compose.

## Running

```bash
cp .env.example .env
docker compose up
```
Swagger UI: http://localhost:8000/docs

## Conventions

- Package manager: `uv` (see `uv.lock`, `pyproject.toml`).
- Linting: `ruff`. Type checking: `mypy`.
- DB migrations: Alembic (`alembic/`).
