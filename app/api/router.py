from fastapi import APIRouter

from app.api.routes import tasks_api, token_api, users_api, utils_api

api_router = APIRouter()

api_router.include_router(token_api.router, prefix="/token", tags=["token"])
api_router.include_router(users_api.router, prefix="/users", tags=["users"])
api_router.include_router(tasks_api.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(utils_api.router, prefix="/utils", tags=["utils"])
