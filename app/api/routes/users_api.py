from typing import List

from fastapi import APIRouter

from app.api.deps import SessionDep
from app.crud.user_crud import crud_user
from app.schemas.user import (
    InfoUser,
    SummaryUser,
    UserCreate,
    UserMe,
    UserUpdate,
    UserUpdateMe,
)

router = APIRouter()


@router.get("/", response_model=List[SummaryUser])
def read_users(
    session: SessionDep,
    skip: int = 0,
    limit: int = 100,
) -> List[SummaryUser]:
    return crud_user.get_multi(db=session, skip=skip, limit=limit)


@router.post("/", response_model=SummaryUser)
def create_user(
    session: SessionDep,
    user: UserCreate,
) -> SummaryUser:
    return crud_user.create(session, obj_in=user)


@router.get("/{user_id}", response_model=InfoUser)
def read_user(
    session: SessionDep,
    user_id: int,
) -> InfoUser:
    return crud_user.get(session, user_id)


@router.put("/{user_id}", response_model=SummaryUser)
def update_user(session: SessionDep, user_id: int, user: UserUpdate) -> SummaryUser:
    return crud_user.update(session, user_id, user)


@router.delete("/{user_id}", response_model={})
def delete_user(session: SessionDep, user_id: int) -> None:
    return crud_user.delete(session, user_id)


@router.get("/me", response_model=UserMe)
def read_user_me(
    session: SessionDep,
) -> UserMe:
    return crud_user.get(session, user_id=1)


@router.put("/me", response_model=UserMe)
def update_user_me(session: SessionDep, user: UserUpdateMe) -> UserMe:
    return crud_user.update_me(session, user)
