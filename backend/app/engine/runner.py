"""
Core run execution and SSE streaming.

Architecture:
  POST /runs  →  execute_run() (background task)
                      │
                      │  queue.put(sse_string)
                      ▼
              asyncio.Queue per run_id
                      │
                      │  queue.get() yields events
                      ▼
  GET /runs/{id}/stream  →  stream_run_events() async generator

NOTE: asyncio.Queue is in-process only. Run uvicorn with --workers 1.
"""
import asyncio
import json
import random
import logging
from typing import AsyncGenerator

from app.database import AsyncSessionLocal
from app.models.run import Run
from app.models.test import Test
from app.models.population import Population
from app.engine.sampler import bootstrap_panel
from app.engine.judge import call_judge
from app.engine.aggregator import aggregate
from app.schemas.common import SubjectResult

logger = logging.getLogger(__name__)

# Global registry of per-run queues
_run_queues: dict[str, asyncio.Queue] = {}


def _get_or_create_queue(run_id: str) -> asyncio.Queue:
    if run_id not in _run_queues:
        _run_queues[run_id] = asyncio.Queue()
    return _run_queues[run_id]


def _format_sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


def _render_prompt(template: str, judge: dict, subject_text: str) -> str:
    prompt = template
    for key, value in judge.items():
        prompt = prompt.replace(f"{{{{{key}}}}}", str(value))
    prompt = prompt.replace("{{text}}", subject_text)
    return prompt


def _build_messages(system: str, prompt: str, image_data_url: str | None) -> list[dict]:
    """Build the messages list for litellm. Adds an image block when image is present."""
    if image_data_url:
        # data URL format: "data:<mime>;base64,<data>"
        media_type = image_data_url.split(";")[0].split(":")[1]
        b64_data = image_data_url.split(",", 1)[1]
        user_content = [
            {"type": "image_url", "image_url": {"url": f"data:{media_type};base64,{b64_data}"}},
            {"type": "text", "text": prompt},
        ]
    else:
        user_content = prompt
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user_content},
    ]


async def execute_run(run_id: str) -> None:
    """
    Background task: execute a run end-to-end, pushing SSE events to the run queue.
    Must open its own DB session (background tasks cannot share the request session).
    """
    queue = _get_or_create_queue(run_id)

    async with AsyncSessionLocal() as session:
        try:
            run: Run | None = await session.get(Run, run_id)
            if run is None:
                logger.error("execute_run: run %s not found", run_id)
                return

            test: Test | None = await session.get(Test, run.test_id)
            if test is None:
                logger.error("execute_run: test %s not found", run.test_id)
                run.status = "error"
                await session.commit()
                return

            population: Population | None = await session.get(Population, test.population_id)
            if population is None:
                logger.error("execute_run: population %s not found", test.population_id)
                run.status = "error"
                await session.commit()
                return

            run.status = "running"
            await session.commit()

            panel = bootstrap_panel(population.dimensions, test.panel_size)
            subjects = test.subjects  # list[dict]
            scale_min = float(test.scale["min"])
            scale_max = float(test.scale["max"])

            total = len(panel) * len(subjects)
            completed = 0

            # Accumulate (subject_id, judge_profile, score, reason, prompt) per subject
            per_subject_scores: dict[str, list[float]] = {s["id"]: [] for s in subjects}
            log_entries: list[dict] = []

            system = (
                "You are a human judge evaluating a subject. "
                "Respond with valid JSON only, using exactly this schema: "
                '{"score": <number>, "reason": "<one sentence>"}. '
                "No other keys, no markdown, no explanation outside the JSON."
            )

            async def judge_one(judge: dict, subject: dict) -> None:
                nonlocal completed
                flipped = random.random() < 0.5
                prompt = _render_prompt(test.prompt_template, judge, subject["text"])
                messages = _build_messages(system, prompt, subject.get("image"))
                score, reason = await call_judge(messages, scale_min, scale_max, flipped)

                per_subject_scores[subject["id"]].append(score)
                log_entries.append(
                    {
                        "subject_id": subject["id"],
                        "judge": judge,
                        "score": score,
                        "reason": reason,
                        "prompt": prompt,
                    }
                )

                completed += 1
                pct = round(completed / total * 100, 1)

                await queue.put(_format_sse("progress", {"completed": completed, "total": total, "pct": pct}))
                await queue.put(_format_sse("judge_result", {"judge": judge, "score": score, "reason": reason}))

            # Fan-out in batches of LLM_BATCH_SIZE
            from app.config import settings

            tasks = [
                judge_one(judge, subject)
                for judge in panel
                for subject in subjects
            ]
            batch_size = settings.LLM_BATCH_SIZE
            for i in range(0, len(tasks), batch_size):
                batch = tasks[i: i + batch_size]
                await asyncio.gather(*batch)

            # Aggregate per subject
            results: list[SubjectResult] = []
            for subject in subjects:
                scores = per_subject_scores[subject["id"]]
                result = aggregate(subject["id"], scores, scale_min, scale_max)
                results.append(result)

            results_dicts = [r.model_dump() for r in results]

            # Compute overall stats across all scores for the complete event
            all_scores = [entry["score"] for entry in log_entries]
            if results:
                first = results[0]
                complete_data = {
                    "mean": first.mean,
                    "median": first.median,
                    "std": first.std,
                    "histogram": first.histogram,
                }
            else:
                complete_data = {"mean": 0.0, "median": 0.0, "std": 0.0, "histogram": []}

            # Persist results
            run.results = results_dicts
            run.panel_size = len(panel)
            run.status = "complete"

            from app.models.run_log import RunLog
            from app.models.base import new_id

            log = RunLog(id=new_id(), run_id=run_id, entries=log_entries)
            session.add(log)
            await session.flush()
            run.log_id = log.id
            await session.commit()

            await queue.put(_format_sse("complete", complete_data))

        except Exception as exc:
            logger.exception("execute_run failed for run %s: %s", run_id, exc)
            try:
                run.status = "error"
                await session.commit()
            except Exception:
                pass
            await queue.put(_format_sse("error", {"message": str(exc)}))
        finally:
            # Sentinel to close the stream
            await queue.put(None)


async def stream_run_events(run_id: str) -> AsyncGenerator[str, None]:
    """
    Async generator that yields raw SSE strings from the run queue.
    Used by GET /runs/{id}/stream.
    """
    queue = _get_or_create_queue(run_id)
    try:
        while True:
            event = await queue.get()
            if event is None:
                break
            yield event
    finally:
        _run_queues.pop(run_id, None)
