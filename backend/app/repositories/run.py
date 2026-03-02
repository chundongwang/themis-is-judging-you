from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.run import Run
from app.models.run_log import RunLog
from app.models.base import new_id


class RunRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list(self) -> list[Run]:
        result = await self.session.execute(select(Run))
        return list(result.scalars().all())

    async def get(self, run_id: str) -> Run | None:
        return await self.session.get(Run, run_id)

    async def create(self, test_id: str, panel_size: int) -> Run:
        run = Run(
            id=new_id(),
            test_id=test_id,
            panel_size=panel_size,
            status="pending",
        )
        self.session.add(run)
        await self.session.commit()
        return run

    async def update_status(self, run_id: str, status: str) -> None:
        run = await self.get(run_id)
        if run:
            run.status = status
            await self.session.commit()

    async def complete(
        self,
        run_id: str,
        results: list[dict],
        entries: list[dict],
        panel_size: int,
    ) -> Run | None:
        run = await self.get(run_id)
        if run is None:
            return None

        log = RunLog(id=new_id(), run_id=run_id, entries=entries)
        self.session.add(log)
        await self.session.flush()

        run.results = results
        run.log_id = log.id
        run.panel_size = panel_size
        run.status = "complete"
        await self.session.commit()
        return run

    async def delete(self, run_id: str) -> bool:
        run = await self.get(run_id)
        if run is None:
            return False
        await self.session.delete(run)
        await self.session.commit()
        return True
