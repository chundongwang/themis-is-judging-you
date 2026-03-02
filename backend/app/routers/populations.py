from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.repositories.population import PopulationRepository
from app.schemas.population import PopulationRead, PopulationCreate, PopulationUpdate

router = APIRouter(prefix="/populations", tags=["populations"])


@router.get("", response_model=list[PopulationRead])
async def list_populations(session: AsyncSession = Depends(get_session)):
    repo = PopulationRepository(session)
    return await repo.list_all()


@router.get("/{population_id}", response_model=PopulationRead)
async def get_population(population_id: str, session: AsyncSession = Depends(get_session)):
    repo = PopulationRepository(session)
    pop = await repo.get(population_id)
    if pop is None:
        raise HTTPException(status_code=404, detail="Population not found")
    return pop


@router.post("", response_model=PopulationRead, status_code=201)
async def create_population(data: PopulationCreate, session: AsyncSession = Depends(get_session)):
    repo = PopulationRepository(session)
    return await repo.create(data)


@router.put("/{population_id}", response_model=PopulationRead)
async def update_population(
    population_id: str,
    data: PopulationUpdate,
    session: AsyncSession = Depends(get_session),
):
    repo = PopulationRepository(session)
    pop = await repo.update(population_id, data)
    if pop is None:
        raise HTTPException(status_code=404, detail="Population not found")
    return pop


@router.delete("/{population_id}", status_code=204)
async def delete_population(population_id: str, session: AsyncSession = Depends(get_session)):
    repo = PopulationRepository(session)
    deleted = await repo.delete(population_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Population not found")
