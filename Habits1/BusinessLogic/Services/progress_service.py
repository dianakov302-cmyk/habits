from database.db import db
from datetime import datetime

progress_collection = db["progress"]


def complete_habit(user_id: str, habit_id: str):

    progress = {
        "userId": user_id,
        "habitId": habit_id,
        "date": datetime.utcnow(),
        "completed": True
    }

    progress_collection.insert_one(progress)

    return {"message": "Habit completed"}


def get_user_progress(user_id: str):

    logs = list(progress_collection.find({"userId": user_id}))

    for log in logs:
        log["_id"] = str(log["_id"])

    return logs