from typing import List

from fastapi import APIRouter

from app.api.deps import SessionDep
from app.crud.task_crud import crud_task
from app.models.tasks_model import Tasks
from app.schemas.task import InfoTask, SummaryTask, Task_Tag, TaskCreate, TaskUpdate
from app.schemas.user import Abst_User

router = APIRouter()


@router.post("/", response_model=InfoTask)
def create_task(
    task: TaskCreate,
    session: SessionDep,
) -> InfoTask:
    return crud_task.create(db=session, obj_in=task, user_id=1)


@router.get("/", response_model=List[SummaryTask])
def read_tasks(
    session: SessionDep,
    skip: int = 0,
    limit: int = 100,
) -> List[SummaryTask]:
    return crud_task.get_all(
        db=session, skip=skip, limit=limit, user_type="user", user_id=1
    )


@router.get("/{task_id}", response_model=InfoTask)
def read_task(
    task_id: int,
    session: SessionDep,
) -> InfoTask:
    return crud_task.get(db=session, id=task_id, user_id=1)


@router.put("/{task_id}", response_model=InfoTask)
def update_task(
    task_id: int,
    task: TaskUpdate,
    session: SessionDep,
) -> InfoTask:
    return crud_task.update(db=session, id=task_id, obj_in=task)


@router.delete("/{task_id}", response_model=None)
def delete_task(
    task_id: int,
    session: SessionDep,
) -> None:
    return crud_task.delete(db=session, id=task_id)


@router.post("/tags", response_model=Task_Tag)
def create_tag(
    tag: Task_Tag,
    session: SessionDep,
) -> Task_Tag:
    return Task_Tag


@router.get("/tags", response_model=List[Task_Tag])
def read_tags(
    session: SessionDep,
    skip: int = 0,
    limit: int = 100,
) -> List[Task_Tag]:
    return List[Task_Tag]


@router.put("/tags/{tag_id}", response_model=Task_Tag)
def update_tag(
    tag_id: int,
    tag: Task_Tag,
    session: SessionDep,
) -> Task_Tag:
    return Task_Tag


@router.delete("/tags/{tag_id}", response_model={})
def delete_tag(
    tag_id: int,
    session: SessionDep,
) -> {}:
    return {}
