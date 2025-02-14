from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from app.core.security import get_password_hash, verify_password
from app.crud.base_crud import CRUDBase
from app.models.tasks_model import (
    Task_Assign,
    Task_Priority,
    Task_Status,
    Task_Tags,
    Tasks,
)
from app.models.users_model import Users
from app.schemas.user import InfoUser, SummaryUser, UserCreate, UserUpdate, UserUpdateMe


class CRUDUser:
    def create(self, db: Session, *, obj_in: UserCreate) -> Users:
        db_obj = Users(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            name=obj_in.name,
            is_active=obj_in.is_active,
            is_admin=obj_in.is_admin,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: int) -> Optional[InfoUser]:
        users = db.query(Users).filter(Users.id == id).first()
        if users:
            assigned_tasks = (
                db.query(Tasks)
                .join(Task_Assign, Task_Assign.task_id == Tasks.id)
                .options(joinedload(Tasks.assign))
                .filter(Task_Assign.user_id == id)
                .all()
            )
            count_wait = len([task for task in assigned_tasks if task.status_id == 0])
            count_work = len([task for task in assigned_tasks if task.status_id == 1])

            response = InfoUser(
                count_wait=count_wait, count_work=count_work, **users.__dict__
            )

        return response

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Users]:
        users = db.query(Users).offset(skip).limit(limit).all()
        print()
        return users

    def get_by_email(self, db: Session, *, email: str) -> Optional[Users]:
        return db.query(Users).filter(Users.email == email).first()

    def update(self, db: Session, *, db_obj: Users, obj_in: UserUpdate) -> Users:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in update_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_me(self, db: Session, *, db_obj: Users, obj_in: UserUpdateMe) -> Users:

        update_data = obj_in.model_dump(exclude_unset=True)
        if obj_in.password:
            hashed_password = get_password_hash(obj_in.password)
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        else:
            update_data["hashed_password"] = db_obj.hashed_password

        for field in update_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> None:
        db.query(Users).filter(Users.id == id).delete()
        db.commit()

    def authenticate(
        self, db: Session, *, email: str, password: str
    ) -> Optional[Users]:
        users = self.get_by_email(db, email=email)
        if not users:
            return None
        if not verify_password(password, users.hashed_password):
            return None
        return users


crud_user = CRUDUser()
