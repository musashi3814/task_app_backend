from sqlalchemy import inspect
from sqlalchemy.orm import Session
from sqlmodel import create_engine

from app.core.config import settings
from app.core.security import get_password_hash

# make sure all SQL Alchemy models are imported before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28
from app.models.base import Base  # noqa: F401
from app.models.tasks import Task_Status
from app.models.users import Users

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

task_status = {
    0: "未着手",
    1: "進行中",
    2: "完了",
}


def init_db(db_session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line

    inspector = inspect(engine)

    if not inspector.has_table("types"):  # "your_table_name"を実際のテーブル名に変更
        # テーブルが存在しない場合、create_all()を実行
        Base.metadata.create_all(bind=engine)

        db_session.add(
            Users(
                name="first",
                email=settings.FIRST_SUPERUSER,
                hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
                is_admin=True,
                is_active=True,
            )
        )

        for data in task_status.items():
            status = Task_Status(id=data[0], name=data[1], color="#FFFFFF")
            db_session.add(status)

        # コミットしてデータを保存
        db_session.commit()
