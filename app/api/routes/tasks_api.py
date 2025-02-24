from typing import List

from fastapi import APIRouter, status

from app.api.deps import CurrentUser, SessionDep
from app.crud.task_crud import crud_task
from app.models.tasks_model import Tasks
from app.schemas.task import InfoTask, SummaryTask, TaskCreate, TaskUpdate
from app.schemas.user import Abst_User

router = APIRouter()


@router.post("/", response_model=InfoTask, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    session: SessionDep,
    current_user: CurrentUser,
) -> InfoTask:
    return crud_task.create(db=session, obj_in=task, user_id=current_user.id)


@router.get("/", response_model=List[SummaryTask], status_code=status.HTTP_200_OK)
def read_tasks(
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
) -> List[SummaryTask]:

    user_type = "admin" if current_user.is_admin else "user"
    return crud_task.get_all(
        db=session, skip=skip, limit=limit, user_type=user_type, user_id=current_user.id
    )


@router.get("/{task_id}", response_model=InfoTask, status_code=status.HTTP_200_OK)
def read_task(
    task_id: int,
    session: SessionDep,
    current_user: CurrentUser,
) -> InfoTask:
    user_type = "admin" if current_user.is_admin else "user"
    return crud_task.get(
        db=session, id=task_id, user_id=current_user.id, user_type=user_type
    )


@router.put("/{task_id}", response_model=InfoTask, status_code=status.HTTP_200_OK)
def update_task(
    task_id: int,
    task: TaskUpdate,
    session: SessionDep,
    current_user: CurrentUser,
) -> InfoTask:
    user_type = "admin" if current_user.is_admin else "user"
    return crud_task.update(
        db=session,
        id=task_id,
        obj_in=task,
        user_id=current_user.id,
        user_type=user_type,
    )


@router.delete(
    "/{task_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(
    task_id: int,
    session: SessionDep,
    current_user: CurrentUser,
) -> None:
    user_type = "admin" if current_user.is_admin else "user"
    return crud_task.delete(
        db=session, id=task_id, user_id=current_user.id, user_type=user_type
    )
