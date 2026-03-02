from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.population import Population
from app.schemas.population import PopulationCreate, PopulationUpdate
from app.models.base import new_id


class PopulationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list(self) -> list[Population]:
        result = await self.session.execute(select(Population))
        return list(result.scalars().all())

    async def get(self, population_id: str) -> Population | None:
        return await self.session.get(Population, population_id)

    async def create(self, data: PopulationCreate) -> Population:
        pop = Population(
            id=data.id or new_id(),
            name=data.name,
            description=data.description,
            dimensions=[d.model_dump() for d in data.dimensions],
        )
        self.session.add(pop)
        await self.session.commit()
        return pop

    async def update(self, population_id: str, data: PopulationUpdate) -> Population | None:
        pop = await self.get(population_id)
        if pop is None:
            return None
        if data.name is not None:
            pop.name = data.name
        if data.description is not None:
            pop.description = data.description
        if data.dimensions is not None:
            pop.dimensions = [d.model_dump() for d in data.dimensions]
        await self.session.commit()
        return pop

    async def delete(self, population_id: str) -> bool:
        pop = await self.get(population_id)
        if pop is None:
            return False
        await self.session.delete(pop)
        await self.session.commit()
        return True
