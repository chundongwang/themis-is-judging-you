from app.routers.populations import router as populations_router
from app.routers.tests import router as tests_router
from app.routers.runs import router as runs_router

__all__ = ["populations_router", "tests_router", "runs_router"]
