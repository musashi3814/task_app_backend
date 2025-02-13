from fastapi import APIRouter

from app.api.routes import tasks, token, users, utils

api_router = APIRouter()

api_router.include_router(token.router, prefix="/token", tags=["token"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
