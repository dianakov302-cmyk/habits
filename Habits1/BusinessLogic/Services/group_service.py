from database.db import db
from bson import ObjectId

groups_collection = db["groups"]


def get_groups():
    groups = list(groups_collection.find())

    for g in groups:
        g["_id"] = str(g["_id"])

    return groups


def create_group(name: str):

    group = {
        "name": name,
        "members": []
    }

    result = groups_collection.insert_one(group)

    return {"message": "Group created", "id": str(result.inserted_id)}


def join_group(group_id: str, user_id: str):

    groups_collection.update_one(
        {"_id": ObjectId(group_id)},
        {"$addToSet": {"members": user_id}}
    )

    return {"message": "Joined group"}