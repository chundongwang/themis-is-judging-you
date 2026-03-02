import random
import math


def _sample_continuous(dist: dict) -> float:
    fn = dist["fn"]
    mu = dist["mu"]
    sigma = dist["sigma"]
    lo = dist["min"]
    hi = dist["max"]

    if fn == "uniform":
        value = random.uniform(lo, hi)
    else:
        # normal and skewed_normal both use gauss; skew is implicit via clamp
        value = random.gauss(mu, sigma)

    return max(lo, min(hi, value))


def _sample_categorical(dist: dict) -> str:
    weights_list = dist["weights"]
    values = [w["value"] for w in weights_list]
    weights = [w["weight"] for w in weights_list]
    return random.choices(values, weights=weights, k=1)[0]


def sample_judge(population_dims: list[dict]) -> dict:
    """Sample one judge profile from a list of dimension configs."""
    profile: dict = {}
    for dim in population_dims:
        dist = dim["distribution"]
        if dim["type"] == "continuous":
            raw = _sample_continuous(dist)
            # Round continuous values to integers for age-like dimensions
            profile[dim["name"]] = int(math.floor(raw))
        else:
            profile[dim["name"]] = _sample_categorical(dist)
    return profile


def bootstrap_panel(dims: list[dict], n: int) -> list[dict]:
    """Generate a panel of N judge profiles sampled from the given dimensions."""
    return [sample_judge(dims) for _ in range(n)]
