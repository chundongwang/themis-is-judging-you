import statistics
import math
from app.schemas.common import SubjectResult


def aggregate(subject_id: str, scores: list[float], scale_min: float, scale_max: float) -> SubjectResult:
    """Compute mean/median/std/histogram for a list of scores."""
    if not scores:
        return SubjectResult(
            subject_id=subject_id,
            mean=0.0,
            median=0.0,
            std=0.0,
            histogram=[],
        )

    mean = statistics.mean(scores)
    median = statistics.median(scores)
    std = statistics.stdev(scores) if len(scores) > 1 else 0.0

    histogram = _build_histogram(scores, scale_min, scale_max)

    return SubjectResult(
        subject_id=subject_id,
        mean=round(mean, 2),
        median=round(median, 2),
        std=round(std, 2),
        histogram=histogram,
    )


def _build_histogram(scores: list[float], scale_min: float, scale_max: float) -> list[dict]:
    """Build 2-unit-wide buckets matching frontend fixture format (e.g. '1-2', '3-4', ...)."""
    buckets: dict[str, int] = {}

    lo = int(math.floor(scale_min))
    hi = int(math.ceil(scale_max))

    # Build bucket labels in order
    bucket_list = []
    start = lo
    while start < hi:
        end = start + 1
        label = f"{start}-{end}"
        bucket_list.append(label)
        buckets[label] = 0
        start += 2

    for score in scores:
        # Find which 2-unit bucket this score falls into
        idx = int(math.floor(score - scale_min))
        bucket_idx = idx // 2
        if 0 <= bucket_idx < len(bucket_list):
            buckets[bucket_list[bucket_idx]] += 1
        elif score >= scale_max:
            buckets[bucket_list[-1]] += 1

    return [{"bucket": label, "count": count} for label, count in buckets.items()]
