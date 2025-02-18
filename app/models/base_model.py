from datetime import datetime
from typing import Any

from sqlalchemy import Column, DateTime, Integer, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    DeclarativeBase,
    ORMExecuteState,
    Session,
    with_loader_criteria,
)

Base = declarative_base()


class CommonColumns:
    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.now(),
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.now(),
        onupdate=datetime.now(),
    )
    deleted_at = Column(DateTime, nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)


# soft_delete用のコード(なぜか動作しない)
@event.listens_for(Session, "do_orm_execute")
def _add_filtering_deleted_at(execute_state: ORMExecuteState) -> None:
    """
    論理削除用のfilterを自動的に適用する
    以下のようにすると、論理削除済のデータも含めて取得可能
    query(...).filter(...).execution_options(include_deleted=True)
    """

    if (
        execute_state.is_select
        and not execute_state.is_column_load
        and not execute_state.is_relationship_load
        and not execute_state.execution_options.get("include_deleted", False)
    ):
        execute_state.statement = execute_state.statement.options(
            with_loader_criteria(
                CommonColumns,
                lambda cls: cls.deleted_at.is_(None),
                include_aliases=True,
            )
        )
