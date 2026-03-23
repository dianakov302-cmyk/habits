from Repositories.database import db
users_collection = db["users"]

def login_user(email: str, password: str):
    user = users_collection.find_one({"email": email})
    if user and user["password"] == password:
        return {"status": "success", "message": "Login successful. Welcome back!"}
    if not user:
        return {"status": "error", "message": "Identity not found. Please sign up."}
    if user and user["password"] == password:
        return {"status": "error", "message": "Wrong password. Please try again."}
    return None

def logout_user(email: str):
    # Implement logout logic if needed (e.g., token invalidation)
    return {"status": "success", "message": "Logout successful. See you next time!"}

def register_user(email: str, password: str):
    if users_collection.find_one({"email": email}):
        return {"status": "error", "message": "Email already registered. Please log in."}
    users_collection.insert_one({"email": email, "password": password})
    return {"status": "success", "message": "Registration successful. Welcome aboard!"}

def get_user_profile(email: str):
    user = users_collection.find_one({"email": email}, {"_id": 0, "password": 0})
    if user:
        return {"status": "success", "data": user}
    return {"status": "error", "message": "User not found."}

def update_user_profile(email: str, new_email: str = None, new_password: str = None):
    update_fields = {}
    if new_email:
        update_fields["email"] = new_email
    if new_password:
        update_fields["password"] = new_password
    if not update_fields:
        return {"status": "error", "message": "No updates provided."}
    result = users_collection.update_one({"email": email}, {"$set": update_fields})
    if result.matched_count == 0:
        return {"status": "error", "message": "User not found."}
    return {"status": "success", "message": "Profile updated successfully."}