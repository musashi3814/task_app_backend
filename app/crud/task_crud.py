from datetime import datetime
from typing import Any, List

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session, joinedload

from app.crud.base_crud import CRUDBase
from app.models.tasks_model import Task_Assign, Tasks
from app.models.users_model import Users
from app.schemas.task import InfoTask, SummaryTask, TaskCreate, TaskUpdate


class Crud_Task:

    def _validate_task_input(
        self, db: Session, obj_in: TaskCreate | TaskUpdate
    ) -> None:
        if obj_in.status_id and obj_in.priority_id:
            if not (0 <= obj_in.status_id <= 2) or not (0 <= obj_in.priority_id <= 2):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="status_idとpriority_idは0~2の範囲で指定してください",
                )
        if obj_in.assigned_id:
            if not isinstance(obj_in.assigned_id, list):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="assigned_idはリストで指定してください",
                )
            if not all(isinstance(uid, int) for uid in obj_in.assigned_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="リスト内の値は全てint型で指定してください",
                )
            if len(obj_in.assigned_id) != len(set(obj_in.assigned_id)):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="assigned_idに重複があります",
                )
            for uid in obj_in.assigned_id:
                if not db.query(Users).filter(Users.id == uid).first():
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"指定されたIDのユーザーが存在しません: {uid}",
                    )

    def create(self, db: Session, *, obj_in: TaskCreate, user_id: int) -> InfoTask:
        self._validate_task_input(db, obj_in)

        db_task_obj = Tasks(
            title=obj_in.title,
            description=obj_in.description,
            due_date=obj_in.due_date,
            status_id=obj_in.status_id,
            priority_id=obj_in.priority_id,
            created_by=user_id,
        )
        db.add(db_task_obj)
        db.commit()
        db.refresh(db_task_obj)

        if obj_in.assigned_id:
            db.add_all(
                [
                    Task_Assign(task_id=db_task_obj.id, user_id=uid)
                    for uid in obj_in.assigned_id
                ]
            )

        db.commit()
        db.refresh(db_task_obj)

        return InfoTask(
            id=db_task_obj.id,
            title=db_task_obj.title,
            description=db_task_obj.description,
            due_date=db_task_obj.due_date,
            status_id=db_task_obj.status_id,
            status=db_task_obj.status.name,
            priority_id=db_task_obj.priority_id,
            priority=db_task_obj.priority.name,
            assigned=obj_in.assigned_id,
            created_at=db_task_obj.created_at,
            created_by=db_task_obj.created_by,
        )

    def get_all(
        self,
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        user_type: str = "user",
    ) -> List[SummaryTask]:
        query = (
            db.query(Tasks)
            .join(Task_Assign, Task_Assign.task_id == Tasks.id)
            .options(
                joinedload(Tasks.status),
                joinedload(Tasks.priority),
                joinedload(Tasks.assign),
            )
            .order_by(Tasks.created_at.desc())
            .offset(skip)
            .limit(limit)
        )

        if user_type == "user":
            query = query.filter(Task_Assign.user_id == user_id)  # only user

        tasks = query.all()

        if not tasks:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="タスクが存在しません"
            )

        response = [
            SummaryTask(
                id=task.id,
                title=task.title,
                due_date=task.due_date,
                status_id=task.status_id,
                status=task.status.name,
                priority_id=task.priority_id,
                priority=task.priority.name,
            )
            for task in tasks
        ]
        return response

    def get(
        self, db: Session, id: int, user_id: int, user_type: str = "user"
    ) -> InfoTask:
        task = (
            db.query(Tasks)
            .options(
                joinedload(Tasks.assign),
                joinedload(Tasks.status),
                joinedload(Tasks.priority),
            )
            .filter(Tasks.id == id)
            .first()
        )
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="指定されたIDのタスクが存在しません",
            )
        if task.assign and user_id not in [assign.user_id for assign in task.assign]:
            if user_type == "user":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="指定されたIDのタスクにアクセス権限がありません",
                )

        response = InfoTask(
            id=task.id,
            title=task.title,
            description=task.description,
            due_date=task.due_date,
            status_id=task.status_id,
            status=task.status.name,
            priority_id=task.priority_id,
            priority=task.priority.name,
            assigned=[assign.user_id for assign in task.assign],
            created_at=task.created_at,
            created_by=task.created_by,
        )
        return response

    def update(
        self, db: Session, id: int, obj_in: TaskUpdate, user_id: int
    ) -> InfoTask:
        self._validate_task_input(db, obj_in)

        loads = [joinedload(Tasks.status), joinedload(Tasks.priority)]

        db_obj = db.query(Tasks).filter(Tasks.id == id).options(*loads).first()
        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="指定されたIDのタスクが存在しません",
            )

        update_data = obj_in.dict(exclude_unset=True)

        db.query(Task_Assign).filter(Task_Assign.task_id == id).delete()
        db.bulk_save_objects(
            [
                Task_Assign(task_id=id, user_id=user_id)
                for user_id in obj_in.assigned_id or []
            ]
        )
        db_obj.updated_by = user_id

        for field, value in update_data.items():
            if field != "assigned_id":
                setattr(db_obj, field, value)

        db.commit()
        db.refresh(db_obj)

        return InfoTask(
            id=db_obj.id,
            title=db_obj.title,
            description=db_obj.description,
            due_date=db_obj.due_date,
            status_id=db_obj.status_id,
            status=db_obj.status.name if db_obj.status else None,
            priority_id=db_obj.priority_id,
            priority=db_obj.priority.name if db_obj.priority else None,
            assigned=(
                [assign.user_id for assign in db_obj.assign] if db_obj.assign else []
            ),
            created_at=db_obj.created_at,
            created_by=db_obj.created_by,
        )

    def delete(self, db: Session, *, id: int, user_id: int) -> None:

        task = db.query(Tasks).filter(Tasks.id == id).first()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="指定されたIDのタスクが存在しません",
            )
        if (
            user_id not in [assign.user_id for assign in task.assign]
            or not task.created_by == user_id
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="指定されたIDのタスクにアクセス権限がありません",
            )

        db.query(Task_Assign).filter(Task_Assign.task_id == id).delete()

        db.delete(task)
        db.commit()


crud_task = Crud_Task()
