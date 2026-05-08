from Habits1.repositories.database import get_collection
from motor.motor_asyncio import AsyncIOMotorClient
from domain.models.user import UserCreate
import bcrypt

class UserRepository:
    def __init__(self):
        self.collection = get_collection("users")

    def create_user(self, user_data: dict):
        # Add default values if not provided
        if "auth_provider" not in user_data:
            user_data["auth_provider"] = "email"
        return self.collection.insert_one(user_data)

    def find_by_email(self, email):
        return self.collection.find_one({"email": email})

    def find_by_id(self, user_id):
        return self.collection.find_one({"_id": user_id})


    from bson import ObjectId
    from datetime import datetime

    class UserRepository:
        def __init__(self, db):
            self.collection = db["users"]  # колекція users у habitplatform

        async def create_user(self, user: UserCreate):
            # Перевіряємо чи існує користувач
            existing = await self.collection.find_one({"email": user.email})
            if existing:
                raise ValueError("Користувач з таким email вже існує")

            # Хешуємо пароль
            hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt(12))

            user_dict = {
                "email": user.email,
                "name": user.name,
                "password": hashed_password,
                "verified": False,
                "created_at": datetime.utcnow()
            }

            result = await self.collection.insert_one(user_dict)
            return {**user_dict, "id": str(result.inserted_id)}
