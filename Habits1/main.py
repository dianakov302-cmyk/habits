from fastapi import FastAPI

# routers
from Controllers.user_controller import router as user_router
from Controllers.progress_controller import router as progress_router
from Controllers.habit_controller import router as habit_router
from Controllers.groups_controller import router as groups_router
from Controllers.challenges_controller import router as challenges_router


app = FastAPI(title="Habits1 API")

app.include_router(user_router)
app.include_router(progress_router)
app.include_router(habit_router)
app.include_router(groups_router)
app.include_router(challenges_router)


@app.get("/", summary="Root")
def root():
    return {"message": "Habits1 API root"}

