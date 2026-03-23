from Repositories.database import db
users_collection = db["users"]
def get_all_habits():

    habits = list(habits_collection.find())

    for habit in habits:
        habit["_id"] = str(habit["_id"])

    return habits

def get_habit_by_id(habit_id):
    habit = habits_collection.find_one({"_id": habit_id})
    if habit:
        habit["_id"] = str(habit["_id"])
        return habit
    return None

def delate_habit(habit_id):
    result = habits_collection.delete_one({"_id": habit_id})
    return result.deleted_count > 0
