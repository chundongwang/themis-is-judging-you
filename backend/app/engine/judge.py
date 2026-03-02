import random
import json
from app.config import settings

FIXTURE_REASONS = [
    "Strong composition and natural lighting make this very appealing.",
    "The subject has striking features that stand out in a positive way.",
    "Clean, professional presentation with good balance.",
    "Average presentation; nothing remarkable but nothing distracting.",
    "Slightly unflattering angle but pleasant overall.",
    "The natural expression feels authentic and relatable.",
    "Good contrast and well-framed subject.",
    "Soft lighting flatters the subject nicely.",
    "The background is a bit busy but the subject is clear.",
    "Unremarkable but competent; meets basic expectations.",
]


async def call_judge(
    prompt: str,
    scale_min: float,
    scale_max: float,
    flipped: bool,
) -> tuple[float, str]:
    """
    Call the LLM judge with a prompt and return (score, reason).

    When STUB_LLM=True returns fixture data.
    When STUB_LLM=False calls LiteLLM with the configured model.

    flipped=True means the question was phrased negatively (e.g. "how unattractive");
    the raw score is inverted: score = (scale_min + scale_max) - raw_score
    """
    if settings.STUB_LLM:
        raw_score = random.uniform(scale_min, scale_max)
        reason = random.choice(FIXTURE_REASONS)
    else:
        import litellm

        response = await litellm.acompletion(
            model=settings.MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=settings.LLM_TEMPERATURE,
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content
        parsed = json.loads(content)
        raw_score = float(parsed["score"])
        reason = str(parsed["reason"])

    if flipped:
        score = (scale_min + scale_max) - raw_score
    else:
        score = raw_score

    score = max(scale_min, min(scale_max, score))
    return round(score, 2), reason
