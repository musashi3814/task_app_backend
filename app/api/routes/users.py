from typing import List

from fastapi import APIRouter

from app.api.deps import SessionDep
from app.schemas.user import InfoUser, SummaryUser, UserCreate, UserMe, UserUpdate

router = APIRouter()


@router.get("/", response_model=List[SummaryUser])
def read_users(
    session: SessionDep,
    skip: int = 0,
    limit: int = 100,
) -> List[SummaryUser]:
    return List[SummaryUser]


@router.post("/", response_model=InfoUser)
def create_user(
    session: SessionDep,
    user: UserCreate,
) -> InfoUser:
    return InfoUser


@router.get("/{user_id}", response_model=InfoUser)
def read_user(
    session: SessionDep,
    user_id: int,
) -> InfoUser:
    return InfoUser


@router.put("/{user_id}", response_model=InfoUser)
def update_user(session: SessionDep, user_id: int, user: UserUpdate) -> InfoUser:
    return InfoUser


@router.delete("/{user_id}", response_model={})
def delete_user(session: SessionDep, user_id: int) -> {}:
    return {}


@router.get("/me", response_model=UserMe)
def read_user_me(
    session: SessionDep,
) -> UserMe:
    return UserMe


@router.put("/me", response_model=UserMe)
def update_user_me(session: SessionDep, user: UserUpdate) -> UserMe:
    return UserMe
