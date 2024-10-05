import datetime
import enum

from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    status: str = "ok"


class CreatedTaskResponse(BaseModel):
    task_id: str


class TaskInfoResponse(BaseModel):
    status: str
    create_time: datetime.datetime
    start_time: datetime.datetime | None = None
    time_to_execute: float | None = None
