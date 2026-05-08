from typing import Any
from Habits1.repositories.user_repository import UserRepository
from .interfaces import IUserService
from Habits1.domain.models.user import UserCreate, UserResponse

class UserService(IUserService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def login_user(self, email: str, password: str):
        try:
            user = self.user_repository.find_by_email(email)
            if user and user["password"] == password:
                return {"status": "success", "message": "Login successful. Welcome back!"}
            if not user:
                return {"status": "error", "message": "Identity not found. Please sign up."}
            return {"status": "error", "message": "Wrong password. Please try again."}
        except Exception as e:
            return {"status": "error", "message": f"Login failed: {str(e)}"}

    def logout_user(self, email: str):
        return {"status": "success", "message": "Logout successful. See you next time!"}

    def register_user(self, email: str, password: str):
        try:
            if self.user_repository.find_by_email(email):
                return {"status": "error", "message": "Email already registered. Please log in."}
            self.user_repository.create_user({"email": email, "password": password})
            return {"status": "success", "message": "Registration successful. Welcome aboard!"}
        except Exception as e:
            return {"status": "error", "message": f"Registration failed: {str(e)}"}

    def get_user_profile(self, email: str):
        try:
            user = self.user_repository.collection.find_one(
                {"email": email},
                {"_id": 0, "password": 0},
            )
            if user:
                return {"status": "success", "data": user}
            return {"status": "error", "message": "User not found."}
        except Exception as e:
            return {"status": "error", "message": f"Failed to fetch profile: {str(e)}"}

    def update_user_profile(self, email: str, new_email: str = None, new_password: str = None):
        try:
            update_fields = {}
            if new_email:
                update_fields["email"] = new_email
            if new_password:
                update_fields["password"] = new_password
            if not update_fields:
                return {"status": "error", "message": "No updates provided."}
            result = self.user_repository.collection.update_one(
                {"email": email},
                {"$set": update_fields},
            )
            if result.matched_count == 0:
                return {"status": "error", "message": "User not found."}
            return {"status": "success", "message": "Profile updated successfully."}
        except Exception as e:
            return {"status": "error", "message": f"Failed to update profile: {str(e)}"}

    def auth_with_google(self, token: str, id_token=None) -> dict[str, Any]:
        try:
            # Перевіряємо токен через Google
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), self.google_client_id
            )

            email = idinfo['email']
            google_id = idinfo['sub']
            name = idinfo.get('name', '')
            picture = idinfo.get('picture', '')

            # Шукаємо користувача в репозиторії
            user = self.user_repository.find_by_email(email)

            if not user:
                # ЕТАП РЕЄСТРАЦІЇ: якщо не знайшли, створюємо новий запит
                self.user_repository.create_user({
                    "email": email,
                    "google_id": google_id,
                    "name": name,
                    "picture": picture,
                    "auth_provider": "google"
                    # Пароль тут не потрібен!
                })
                return {"status": "success", "message": "Акаунт створено! Ласкаво просимо до Anaida Space."}

            # ЕТАП АВТОРИЗАЦІЇ: якщо знайшли, просто впускаємо
            return {"status": "success", "message": "З поверненням!"}

        except ValueError:
            return {"status": "error", "message": "Невалідний токен Google."}

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register(self, user_data: UserCreate) -> UserResponse:
        user = await self.user_repo.create_user(user_data)
        # Видаляємо пароль перед поверненням
        if "password" in user:
            del user["password"]
        return UserResponse(**user)