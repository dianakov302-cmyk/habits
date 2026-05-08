from pydantic import BaseModel, Field


class UserCredentialsRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=320)
    password: str = Field(..., min_length=1)


class UserLogoutRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=320)


class UserProfileUpdateRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=320)
    new_email: str | None = Field(default=None, min_length=3, max_length=320)
    new_password: str | None = Field(default=None, min_length=1)


class HabitCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=1000)


class GroupCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)


class GroupJoinRequest(BaseModel):
    group_id: str = Field(..., min_length=1)
    user_id: str = Field(..., min_length=1)


class ChallengeCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)


class HabitCompletionRequest(BaseModel):
    user_id: str = Field(..., min_length=1)
    habit_id: str = Field(..., min_length=1)


class GoalCreateRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=320)
    goal_code: str = Field(..., min_length=1, max_length=100)
