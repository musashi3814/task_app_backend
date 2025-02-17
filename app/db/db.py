from sqlalchemy import inspect
from sqlalchemy.orm import Session
from sqlmodel import create_engine

from app.core.config import settings
from app.core.security import get_password_hash

# make sure all SQL Alchemy models are imported before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28
from app.models.base_model import Base  # noqa: F401
from app.models.tasks_model import Task_Priority, Task_Status
from app.models.users_model import Users

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI), echo=True)

task_status = {
    0: "未着手",
    1: "進行中",
    2: "完了",
}

task_priority = {
    0: "低",
    1: "中",
    2: "高",
}


def init_db(db_session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line

    inspector = inspect(engine)

    if not inspector.has_table("types"):  # "your_table_name"を実際のテーブル名に変更
        # テーブルが存在しない場合、create_all()を実行
        Base.metadata.create_all(bind=engine)

        if (
            not db_session.query(Users)
            .filter(Users.email == settings.FIRST_SUPERUSER)
            .first()
        ):
            db_session.add(
                Users(
                    name="first",
                    email=settings.FIRST_SUPERUSER,
                    hashed_password=get_password_hash(
                        settings.FIRST_SUPERUSER_PASSWORD
                    ),
                    is_admin=True,
                    is_active=True,
                    created_by=1,
                )
            )

        for data in task_status.items():
            if (
                not db_session.query(Task_Status)
                .filter(Task_Status.id == data[0])
                .first()
            ):
                status = Task_Status(id=data[0], name=data[1], color="#FFFFFF")
                db_session.add(status)

        for data in task_priority.items():
            if (
                not db_session.query(Task_Priority)
                .filter(Task_Priority.id == data[0])
                .first()
            ):
                priority = Task_Priority(id=data[0], name=data[1], color="#FFFFFF")
                db_session.add(priority)

        # コミットしてデータを保存
        db_session.commit()
