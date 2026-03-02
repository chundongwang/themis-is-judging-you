"""
Seed script — idempotent. Populates fixture populations and tests.

Run: python -m scripts.seed
"""
import asyncio
import sys
import os

# Allow running from backend/ directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import AsyncSessionLocal, engine
from app.models import Base, Population, Test


POPULATIONS = [
    {
        "id": "us-general",
        "name": "United States General Public",
        "description": "Broad US demographic sample across age, gender, income, and region.",
        "dimensions": [
            {
                "name": "age",
                "type": "continuous",
                "distribution": {"fn": "normal", "mu": 38, "sigma": 15, "min": 18, "max": 80},
            },
            {
                "name": "gender",
                "type": "categorical",
                "distribution": {
                    "fn": "weighted",
                    "weights": [
                        {"value": "Male", "weight": 0.49},
                        {"value": "Female", "weight": 0.49},
                        {"value": "Non-binary", "weight": 0.02},
                    ],
                },
            },
            {
                "name": "occupation",
                "type": "categorical",
                "distribution": {
                    "fn": "weighted",
                    "weights": [
                        {"value": "Professional", "weight": 0.3},
                        {"value": "Creative", "weight": 0.2},
                        {"value": "Trades", "weight": 0.2},
                        {"value": "Student", "weight": 0.15},
                        {"value": "Retired", "weight": 0.15},
                    ],
                },
            },
        ],
    },
    {
        "id": "cn-mainland",
        "name": "China Mainland Urban",
        "description": "Urban Chinese demographic sample skewed toward younger professionals.",
        "dimensions": [
            {
                "name": "age",
                "type": "continuous",
                "distribution": {"fn": "normal", "mu": 29, "sigma": 8, "min": 18, "max": 60},
            },
            {
                "name": "gender",
                "type": "categorical",
                "distribution": {
                    "fn": "weighted",
                    "weights": [
                        {"value": "Male", "weight": 0.51},
                        {"value": "Female", "weight": 0.49},
                    ],
                },
            },
        ],
    },
]

TESTS = [
    {
        "id": "test-001",
        "name": "Headshot Attractiveness",
        "created_at": "2026-02-28T13:00:00+00:00",
        "prompt_template": (
            "You are a {{gender}}, aged {{age}}, working as {{occupation}}. "
            "Rate the attractiveness of the following person on a scale from 1 to 10. "
            "Respond with just the number and one sentence reason.\n\nPerson: {{text}}"
        ),
        "scale": {"min": 1, "max": 10, "label": "attractiveness"},
        "population_id": "us-general",
        "panel_size": 20,
        "subjects": [
            {
                "id": "subject-1",
                "text": "A person with warm brown eyes and a natural smile.",
                "image": None,
            }
        ],
    },
    {
        "id": "test-002",
        "name": "Profile Photo Quality",
        "created_at": "2026-02-27T09:00:00+00:00",
        "prompt_template": (
            "You are a {{gender}}, aged {{age}}. "
            "Rate the quality of this profile photo on a scale of 1-10."
        ),
        "scale": {"min": 1, "max": 10, "label": "quality"},
        "population_id": "cn-mainland",
        "panel_size": 10,
        "subjects": [
            {
                "id": "subject-2",
                "text": "A professional headshot with neutral background.",
                "image": None,
            }
        ],
    },
]


async def seed() -> None:
    # Ensure tables exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        for pop_data in POPULATIONS:
            existing = await session.get(Population, pop_data["id"])
            if existing is None:
                pop = Population(**pop_data)
                session.add(pop)
                print(f"Inserted population: {pop_data['id']}")
            else:
                print(f"Skipped population (exists): {pop_data['id']}")

        for test_data in TESTS:
            from datetime import datetime, timezone
            td = dict(test_data)
            td["created_at"] = datetime.fromisoformat(td["created_at"])
            existing = await session.get(Test, td["id"])
            if existing is None:
                test = Test(**td)
                session.add(test)
                print(f"Inserted test: {td['id']}")
            else:
                print(f"Skipped test (exists): {td['id']}")

        await session.commit()
    print("Seed complete.")


if __name__ == "__main__":
    asyncio.run(seed())
