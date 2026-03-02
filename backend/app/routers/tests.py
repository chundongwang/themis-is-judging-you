from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.repositories.test import TestRepository
from app.schemas.test import TestRead, TestCreate, TestUpdate

router = APIRouter(prefix="/tests", tags=["tests"])


@router.get("", response_model=list[TestRead])
async def list_tests(session: AsyncSession = Depends(get_session)):
    repo = TestRepository(session)
    return await repo.list_all()


@router.get("/{test_id}", response_model=TestRead)
async def get_test(test_id: str, session: AsyncSession = Depends(get_session)):
    repo = TestRepository(session)
    test = await repo.get(test_id)
    if test is None:
        raise HTTPException(status_code=404, detail="Test not found")
    return test


@router.post("", response_model=TestRead, status_code=201)
async def create_test(data: TestCreate, session: AsyncSession = Depends(get_session)):
    repo = TestRepository(session)
    return await repo.create(data)


@router.put("/{test_id}", response_model=TestRead)
async def update_test(
    test_id: str,
    data: TestUpdate,
    session: AsyncSession = Depends(get_session),
):
    repo = TestRepository(session)
    test = await repo.update(test_id, data)
    if test is None:
        raise HTTPException(status_code=404, detail="Test not found")
    return test


@router.delete("/{test_id}", status_code=204)
async def delete_test(test_id: str, session: AsyncSession = Depends(get_session)):
    repo = TestRepository(session)
    deleted = await repo.delete(test_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Test not found")
