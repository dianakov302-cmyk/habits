from database.db import db
from bson import ObjectId

challenges_collection = db["challenges"]


def get_challenges():
    challenges = list(challenges_collection.find())

    for c in challenges:
        c["_id"] = str(c["_id"])

    return challenges


def create_challenge(title: str):

    challenge = {"title": title}

    result = challenges_collection.insert_one(challenge)

    return {
        "message": "Challenge created",
        "id": str(result.inserted_id)
    }