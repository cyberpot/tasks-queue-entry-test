import datetime
import enum

from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    status: str = "ok"


class CreatedTaskResponse(BaseModel):
    task_id: str


class TaskInfoResponse(BaseModel):
    status: str
    create_time: str
    start_time: datetime.datetime
    time_to_execute: float
