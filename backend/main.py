import sys
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.business_logic.services.challenge_service import ChallengeService
from backend.business_logic.services.goal_service import GoalService
from backend.business_logic.services.groups_service import GroupService
from backend.business_logic.services.habit_service import HabitService
from backend.business_logic.services.progress_service import ProgressService
from backend.business_logic.services.user_service import UserService
from backend.controllers.challenges_controller import (
    create_router as create_challenges_router,
)
from backend.controllers.goal_controller import create_router as create_goal_router
from backend.controllers.groups_controller import create_router as create_groups_router
from backend.controllers.habit_controller import create_router as create_habit_router
from backend.controllers.progress_controller import create_router as create_progress_router
from backend.controllers.user_controller import create_router as create_user_router
from backend.repositories.challenge_repository import PostRepository
from backend.repositories.database import ping_database
from backend.repositories.goal_repository import GoalRepository
from backend.repositories.groups_repository import GroupRepository
from backend.repositories.habit_repository import HabitRepository
from backend.repositories.progress_repository import ProgressRepository
from backend.repositories.user_repository import UserRepository

load_dotenv()

STATIC_DIR = Path(__file__).resolve().parents[1] / "frontend" / "site"



class Container:
    def __init__(self):
        self._user_repository = None
        self._habit_repository = None
        self._group_repository = None
        self._challenge_repository = None
        self._progress_repository = None
        self._goal_repository = None

        self._user_service = None
        self._habit_service = None
        self._group_service = None
        self._challenge_service = None
        self._progress_service = None
        self._goal_service = None

    def get_user_service(self):
        if self._user_service is None:
            self._user_repository = self._user_repository or UserRepository()
            self._user_service = UserService(self._user_repository)
        return self._user_service

    def get_habit_service(self):
        if self._habit_service is None:
            self._habit_repository = self._habit_repository or HabitRepository()
            self._habit_service = HabitService(self._habit_repository)
        return self._habit_service

    def get_group_service(self):
        if self._group_service is None:
            self._group_repository = self._group_repository or GroupRepository()
            self._group_service = GroupService(self._group_repository)
        return self._group_service

    def get_challenge_service(self):
        if self._challenge_service is None:
            self._challenge_repository = self._challenge_repository or PostRepository()
            self._challenge_service = ChallengeService(self._challenge_repository)
        return self._challenge_service

    def get_progress_service(self):
        if self._progress_service is None:
            self._progress_repository = self._progress_repository or ProgressRepository()
            self._progress_service = ProgressService(self._progress_repository)
        return self._progress_service

    def get_goal_service(self):
        if self._goal_service is None:
            self._goal_repository = self._goal_repository or GoalRepository()
            self._goal_service = GoalService(self._goal_repository)
        return self._goal_service


def create_app() -> FastAPI:
    container = Container()

    app = FastAPI(
        title="backend API",
        version="1.0.0",
        description="API server for habits, progress tracking, groups, challenges, and users.",
    )

    app.state.container = container

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(create_user_router(container.get_user_service))
    app.include_router(create_progress_router(container.get_progress_service))
    app.include_router(create_habit_router(container.get_habit_service))
    app.include_router(create_groups_router(container.get_group_service))
    app.include_router(create_challenges_router(container.get_challenge_service))
    app.include_router(create_goal_router(container.get_goal_service))
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    @app.get("/", summary="Root")
    def root():
        return {
            "message": "backend API is running",
            "docs": "/docs",
            "health": "/health",
            "ui": "/app",
        }

    @app.get("/app", summary="Web UI")
    def web_app():
        return FileResponse(STATIC_DIR / "index.html")

    @app.get("/health", summary="Health Check")
    def health():
        is_connected = ping_database()
        return {
            "status": "ok" if is_connected else "degraded",
            "database": "connected" if is_connected else "unavailable",
        }

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8080, reload=True)
