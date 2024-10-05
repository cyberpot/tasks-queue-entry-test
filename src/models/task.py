import datetime
import enum

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from models.base import BaseModel


class TaskStatuses(enum.StrEnum):
    in_queue = "In Queue"
    run = "Run",
    completed = "Completed",


class TaskModel(BaseModel):

    __tablename__ = "task_model"

    status: Mapped[TaskStatuses] = mapped_column(
        default=TaskStatuses.in_queue.value
    )

    start_time: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        nullable=True,
        server_default=None,
    )
    exec_time: Mapped[float] = mapped_column(
        nullable=True,
        server_default=None,
    )
