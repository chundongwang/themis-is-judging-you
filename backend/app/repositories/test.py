from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.test import Test
from app.schemas.test import TestCreate, TestUpdate
from app.models.base import new_id


class TestRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_all(self) -> list[Test]:
        result = await self.session.execute(select(Test))
        return list(result.scalars().all())

    async def get(self, test_id: str) -> Test | None:
        return await self.session.get(Test, test_id)

    async def create(self, data: TestCreate) -> Test:
        test = Test(
            id=data.id or new_id(),
            name=data.name,
            prompt_template=data.prompt_template,
            scale=data.scale.model_dump(),
            population_id=data.population_id,
            panel_size=data.panel_size,
            subjects=[s.model_dump() for s in data.subjects],
        )
        self.session.add(test)
        await self.session.commit()
        return test

    async def update(self, test_id: str, data: TestUpdate) -> Test | None:
        test = await self.get(test_id)
        if test is None:
            return None
        if data.name is not None:
            test.name = data.name
        if data.prompt_template is not None:
            test.prompt_template = data.prompt_template
        if data.scale is not None:
            test.scale = data.scale.model_dump()
        if data.population_id is not None:
            test.population_id = data.population_id
        if data.panel_size is not None:
            test.panel_size = data.panel_size
        if data.subjects is not None:
            test.subjects = [s.model_dump() for s in data.subjects]
        await self.session.commit()
        return test

    async def delete(self, test_id: str) -> bool:
        test = await self.get(test_id)
        if test is None:
            return False
        await self.session.delete(test)
        await self.session.commit()
        return True
