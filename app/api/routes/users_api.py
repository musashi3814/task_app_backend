from typing import List

from fastapi import APIRouter, HTTPException, status

from app.api.deps import CurrentAdminUser, CurrentUser, SessionDep
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


@router.post("/", response_model=SummaryUser, status_code=status.HTTP_201_CREATED)
def create_user(
    session: SessionDep,
    current_user: CurrentAdminUser,
    user: UserCreate,
) -> SummaryUser:

    exist_user = crud_user.get_by_email(session, email=user.email)
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="そのメールアドレスは既に登録されています",
        )
    return crud_user.create(db=session, obj_in=user, user_id=current_user.id)


@router.get("/", response_model=List[SummaryUser], status_code=status.HTTP_200_OK)
def read_users(
    session: SessionDep,
    current_user: CurrentAdminUser,
    skip: int = 0,
    limit: int = 100,
) -> List[SummaryUser]:
    return crud_user.get_multi(db=session, skip=skip, limit=limit)


@router.get("/me", response_model=UserMe, status_code=status.HTTP_200_OK)
def read_user_me(
    session: SessionDep,
    current_user: CurrentUser,
) -> UserMe:
    return current_user


@router.put("/me", response_model=UserMe, status_code=status.HTTP_200_OK)
def update_user_me(
    session: SessionDep, current_user: CurrentUser, user: UserUpdateMe
) -> UserMe:
    if user.email:
        existing_user = crud_user.get_by_email(session, email=user.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="そのメールアドレスは既に登録されています",
            )

    return crud_user.update_me(db=session, id=current_user.id, obj_in=user)


@router.get("/{user_id}", response_model=InfoUser, status_code=status.HTTP_200_OK)
def read_user(
    session: SessionDep,
    current_user: CurrentAdminUser,
    user_id: int,
) -> InfoUser:
    return crud_user.get(db=session, id=user_id)


@router.put("/{user_id}", response_model=SummaryUser, status_code=status.HTTP_200_OK)
def update_user(
    session: SessionDep, current_user: CurrentAdminUser, user_id: int, user: UserUpdate
) -> SummaryUser:

    return crud_user.update(
        db=session, id=user_id, obj_in=user, user_id=current_user.id
    )


@router.delete(
    "/{user_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT
)
def delete_user(
    session: SessionDep, current_user: CurrentAdminUser, user_id: int
) -> None:

    user = crud_user.get(db=session, id=user_id)
    if not current_user.is_admin or user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="削除する権限がありません",
        )
    return crud_user.delete(db=session, id=user_id)
