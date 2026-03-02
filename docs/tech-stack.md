# Tech Stack

## Overview

The architecture is split into a static frontend and a thin Python backend. The frontend handles UI and orchestrates user interactions; the backend owns the judging pipeline, LLM calls, and data persistence.

---

## Frontend

**React + Vite** — static build, hosted on Vercel.

- Vite produces a fully static bundle, which works cleanly with both Vercel (web) and Capacitor (native) without SSR friction.
- Next.js is intentionally avoided — its SSR model is wasted complexity when all data comes from API calls, and it creates friction with Capacitor's static packaging requirement.

**Capacitor** — wraps the Vite/React app for iOS and Android.

- Same codebase, same UI. Native is a packaging step, not a separate app.
- Added when native distribution is needed; doesn't affect frontend architecture.

**EventSource (SSE)** — browser-native API for receiving streaming progress from the backend.

- No extra libraries needed.
- Works in mobile browsers and Capacitor.

---

## Backend

**Python + FastAPI** — hosted on Railway.

- Railway is simpler and cheaper than AWS/Azure for this scale: deploy a Python container, managed Postgres included, no devops overhead.
- FastAPI has native SSE support via `StreamingResponse`.
- Railway supports long-lived connections — unlike Vercel serverless functions which have a 10s timeout that would cut off SSE streams mid-run.

**LiteLLM** — unified interface over all LLM providers.

- Identical call signatures across Claude, Gemini, GPT-4o, and local models.
- Swap models by changing a single string: `model="claude-opus-4-6"` → `model="gemini/gemini-2.0-flash"`.
- No lock-in to Anthropic or any single provider.

**asyncio** — native Python async for parallel LLM fan-out.

- All judge calls are independent; `asyncio.gather` handles parallelism with no framework overhead.
- Runs in batches to respect API rate limits:

```python
async def run_batch(tasks, batch_size=100):
    for i in range(0, len(tasks), batch_size):
        batch = tasks[i : i + batch_size]
        await asyncio.gather(*[call_llm(t) for t in batch])
```

- No Temporal or task queue needed at this scale. Can be added later if runs grow to require durable multi-hour execution or cross-restart resume.

**Postgres** — managed by Railway.

- Stores populations, tests, judge profile indexes, runs, aggregated results, and run logs.

---

## Progress Streaming

Runs are long — N parallel LLM calls take time. The frontend stays live via **Server-Sent Events (SSE)**:

```
POST /runs              → creates the run, returns run_id
GET  /runs/{id}/stream  → SSE stream, open until run completes
```

The backend emits events as each judge finishes:

```
event: progress
data: {"completed": 45, "total": 100, "pct": 45}

event: judge_result
data: {"judge": {"age": 28, "gender": "Female", "occupation": "Creative"}, "score": 8, "reason": "Strong composition and natural lighting."}

event: complete
data: {"mean": 7.2, "median": 7.5, "std": 1.1, "histogram": [...]}
```

This lets the UI show live individual judge opinions as they arrive — not just a progress bar — while the full aggregated result is delivered at the end.

---

## Stack Summary

| Layer       | Technology         | Hosting   |
|-------------|--------------------|-----------|
| Frontend    | React + Vite       | Vercel    |
| Native      | Capacitor          | App Store / Play Store |
| Backend     | Python + FastAPI   | Railway   |
| LLM calls   | LiteLLM            | —         |
| Parallelism | asyncio            | —         |
| Streaming   | SSE (EventSource)  | —         |
| Database    | Postgres           | Railway   |

---

## Future Considerations

- **OLAP / analytics**: Run log entries (one row per judge × subject) are a natural fit for a columnar store like ClickHouse or Druid for slice-and-dice aggregations across demographic dimensions.
- **Task queue**: If panel sizes grow large (e.g. 10,000+ judges) or runs need to survive server restarts, BullMQ or Temporal can be layered in without changing the core flow.
- **Model routing**: LiteLLM supports routing rules (e.g. use Gemini for cost, Claude for quality) and fallbacks — useful once the product needs cost optimisation.
