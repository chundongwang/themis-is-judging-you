# Country Simulator

Simulate a diverse panel of LLM-driven judges to rate any subject — headshots, profile photos, product images — across configurable demographic populations.

## Architecture

```
frontend/   React + Vite (Vercel)
backend/    Python + FastAPI (Railway)
```

The frontend is a fully static build. All data lives in the backend. Progress streams to the browser in real time via **Server-Sent Events**.

---

## Prerequisites

- **Node.js** 20+ and **npm**
- **Python** 3.11+
- **uv** — [install](https://docs.astral.sh/uv/getting-started/installation/): `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Git**

---

## Local Development

### 1. Clone

```sh
git clone <repo-url>
cd country-simulator
```

### 2. Backend

```sh
cd backend

# Create venv and install dependencies
uv sync

# Copy the env template and edit as needed
cp .env.example .env

# Seed the database with fixture populations and tests
uv run python -m scripts.seed

# Start the dev server
# --workers 1 is required — the SSE bridge uses an in-process asyncio.Queue
uv run uvicorn app.main:app --reload --port 8000 --workers 1
```

The API is now at `http://localhost:8000`. Tables are auto-created on first startup.

**Verify it works:**
```sh
curl http://localhost:8000/health
# → {"status":"ok"}

curl http://localhost:8000/populations
# → [{...}, {...}]
```

### 3. Frontend

```sh
cd frontend
npm install
npm run dev
```

The app is now at `http://localhost:5173`. It proxies `/api/*` to `http://localhost:8000` — see `vite.config.ts`.

> The frontend ships with a mock API layer. To switch to the real backend, update `frontend/src/api/client.ts` to point at the local server.

---

## Environment Variables

All backend config lives in `backend/.env` (copy from `backend/.env.example`):

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `sqlite+aiosqlite:///./dev.db` | SQLite for dev, Postgres for prod |
| `MODEL` | `claude-sonnet-4-6` | LiteLLM model string |
| `LLM_TEMPERATURE` | `0.7` | Judge response temperature |
| `LLM_BATCH_SIZE` | `100` | Max concurrent LLM calls per batch |
| `CORS_ORIGINS` | `["http://localhost:5173"]` | Allowed frontend origins |
| `STUB_LLM` | `true` | Use fixture data instead of real LLM calls |
| `DEBUG` | `true` | SQLAlchemy query logging |

### Enabling real LLM calls

Set `STUB_LLM=false` and add your provider API key:

```sh
# backend/.env
STUB_LLM=false
MODEL=claude-sonnet-4-6
ANTHROPIC_API_KEY=sk-ant-...

# Or use a different provider:
# MODEL=gemini/gemini-2.0-flash
# GEMINI_API_KEY=...

# MODEL=gpt-4o
# OPENAI_API_KEY=sk-...
```

LiteLLM handles all providers with the same interface — swap `MODEL` to switch.

---

## Running a Test

1. Open `http://localhost:5173`
2. Select a test (e.g. *Headshot Attractiveness*)
3. Click **Run** — a POST to `/runs` creates the run and starts the background task
4. Watch the Results page stream live judge scores via SSE
5. The final aggregated result (mean, median, std, histogram) appears when the run completes

To watch the raw SSE stream:
```sh
# Start a run first, copy the returned id
curl -X POST http://localhost:8000/runs \
  -H "Content-Type: application/json" \
  -d '{"test_id":"test-001"}'

# Stream it
curl -N http://localhost:8000/runs/<id>/stream
```

---

## Database Migrations (Alembic)

Dev uses `Base.metadata.create_all` on startup — no migration needed.

For production schema changes:

```sh
cd backend

# Generate a migration from model changes
DATABASE_URL=<prod-url> uv run alembic revision --autogenerate -m "describe change"

# Apply migrations
DATABASE_URL=<prod-url> uv run alembic upgrade head
```

---

## Deployment

See [`docs/setup-accounts.md`](docs/setup-accounts.md) for one-time account setup on Vercel, Railway, and LLM providers.

### Frontend → Vercel

```sh
cd frontend
npm run build
vercel deploy
```

### Backend → Railway

Push to `main` — Railway auto-deploys from the `backend/` directory.

Set these environment variables in the Railway service dashboard:
- `STUB_LLM=false`
- `MODEL=<model-string>`
- Provider API key (`ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, or `OPENAI_API_KEY`)
- `DATABASE_URL` is injected automatically by the Railway Postgres plugin
- `CORS_ORIGINS=["https://<your-vercel-domain>"]`

Start command: `uv run uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1`

---

## Project Structure

```
country-simulator/
├── frontend/
│   ├── src/
│   │   ├── api/          # mock API (swap for real fetch calls)
│   │   ├── components/   # UI primitives + feature components
│   │   ├── hooks/        # useSSE, etc.
│   │   ├── lib/          # types.ts
│   │   └── pages/        # Home, Results, Populations, History
│   └── package.json
├── backend/
│   ├── app/
│   │   ├── config.py     # pydantic-settings
│   │   ├── main.py       # app factory, CORS, lifespan
│   │   ├── models/       # SQLAlchemy ORM
│   │   ├── schemas/      # Pydantic v2
│   │   ├── repositories/ # async CRUD
│   │   ├── routers/      # HTTP endpoints
│   │   └── engine/       # sampler, judge, aggregator, runner
│   ├── scripts/seed.py   # fixture data
│   ├── pyproject.toml
│   └── uv.lock           # generated on first uv sync
└── docs/
    ├── tech-stack.md
    ├── judge-algorithm.md
    └── data-structures.md
```

---

## Key Design Notes

- **`--workers 1` is required** — the SSE stream uses an `asyncio.Queue` per run, which is in-process only. Multi-worker deployments would need Redis pub/sub instead.
- **JSON columns** — population dimensions, test subjects, and run results are stored as JSON blobs, not relational tables. Pydantic v2 deserialises them transparently.
- **Question flipping** — half of judge calls use a negatively-framed prompt (e.g. "how unattractive") with the score inverted. This cancels acquiescence bias. See `docs/judge-algorithm.md`.
