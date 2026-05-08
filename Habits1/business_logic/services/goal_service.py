from datetime import UTC, datetime

from Habits1.repositories.goal_repository import GoalRepository
from .interfaces import IGoalService


class GoalService(IGoalService):
    GOAL_OPTIONS = [
        {
            "code": "focus_productivity",
            "title": "Focus & Productivity",
            "description": "Improve concentration and reduce distractions to get more done daily.",
            "schedule": "Daily work sessions",
        },
        {
            "code": "nutrition",
            "title": "Nutrition",
            "description": "Fuel your body with the right food for energy and health.",
            "schedule": "Every meal",
        },
        {
            "code": "self_discipline",
            "title": "Self-Discipline",
            "description": "Build a consistent routine for workouts, movement, and healthy sleep.",
            "schedule": "Daily",
        },
        {
            "code": "studying",
            "title": "Studying",
            "description": "Learn faster and more effectively.",
            "schedule": "Daily study blocks",
        },
        {
            "code": "find_people",
            "title": "Find your person / people",
            "description": "Connect with like-minded individuals on the same journey.",
            "schedule": "Weekly community check-in",
        },
        {
            "code": "find_direction",
            "title": "Find Identity / Direction",
            "description": "Discover your true purpose and path.",
            "schedule": "Daily reflection",
        },
        {
            "code": "health",
            "title": "Health",
            "description": "Prioritize your physical and mental well-being.",
            "schedule": "Daily",
        },
    ]

    def __init__(self, goal_repository: GoalRepository):
        self.goal_repository = goal_repository
        self._options_by_code = {
            option["code"]: option for option in self.GOAL_OPTIONS
        }

    def get_goal_options(self) -> dict[str, list[dict[str, str]]]:
        return {"status": "success", "data": self.GOAL_OPTIONS}

    def set_goal(self, email: str, goal_code: str) -> dict[str, str | dict]:
        goal_option = self._options_by_code.get(goal_code)
        if goal_option is None:
            return {"status": "error", "message": "Goal code is not supported."}

        goal_data = {
            "email": email,
            "goalCode": goal_option["code"],
            "goalTitle": goal_option["title"],
            "goalDescription": goal_option["description"],
            "schedule": goal_option["schedule"],
            "updatedAt": datetime.now(UTC).isoformat(),
        }
        try:
            self.goal_repository.upsert_goal(email, goal_data)
            return {
                "status": "success",
                "message": "Goal saved successfully.",
                "data": goal_data,
            }
        except Exception as e:
            return {"status": "error", "message": f"Failed to save goal: {str(e)}"}

    def get_user_goal(self, email: str) -> dict[str, str | dict]:
        try:
            goal = self.goal_repository.find_by_email(email)
            if goal is None:
                return {"status": "error", "message": "Goal not found."}

            goal["_id"] = str(goal["_id"])
            return {"status": "success", "data": goal}
        except Exception as e:
            return {"status": "error", "message": f"Failed to fetch goal: {str(e)}"}
