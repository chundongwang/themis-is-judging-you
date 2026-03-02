from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.repositories.run import RunRepository
from app.repositories.test import TestRepository
from app.schemas.run import RunRead, RunCreate
from app.engine.runner import execute_run, stream_run_events

router = APIRouter(prefix="/runs", tags=["runs"])


@router.get("", response_model=list[RunRead])
async def list_runs(session: AsyncSession = Depends(get_session)):
    repo = RunRepository(session)
    return await repo.list_all()


@router.get("/{run_id}", response_model=RunRead)
async def get_run(run_id: str, session: AsyncSession = Depends(get_session)):
    repo = RunRepository(session)
    run = await repo.get(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return run


@router.post("", response_model=RunRead, status_code=201)
async def create_run(
    data: RunCreate,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
):
    test_repo = TestRepository(session)
    test = await test_repo.get(data.test_id)
    if test is None:
        raise HTTPException(status_code=404, detail="Test not found")

    run_repo = RunRepository(session)
    run = await run_repo.create(test_id=data.test_id, panel_size=test.panel_size)

    background_tasks.add_task(execute_run, run.id)
    return run


@router.get("/{run_id}/stream")
async def stream_run(run_id: str, session: AsyncSession = Depends(get_session)):
    run_repo = RunRepository(session)
    run = await run_repo.get(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")

    return StreamingResponse(
        stream_run_events(run_id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@router.delete("/{run_id}", status_code=204)
async def delete_run(run_id: str, session: AsyncSession = Depends(get_session)):
    repo = RunRepository(session)
    deleted = await repo.delete(run_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Run not found")
