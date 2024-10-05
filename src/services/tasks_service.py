import dataclasses
from datetime import datetime

from managers.tasks_sql_manager import TasksSQLManager


@dataclasses.dataclass(frozen=True)
class TaskInfo:
    status: str
    create_time: datetime
    start_time: datetime | None
    time_to_execute: float | None


class TasksService:
    def __init__(self, sql_manager: TasksSQLManager):
        self._sql_manager = sql_manager

    @property
    def sql_manager(self) -> TasksSQLManager:
        return self._sql_manager

    async def get_task_info(self, instance_id) -> dict | None:
        instance = await self.sql_manager.get_by_id(instance_id=instance_id)
        if instance is None:
            return None
        return dataclasses.asdict(TaskInfo(
            status=instance.status,
            create_time=instance.create_time,
            start_time=instance.start_time,
            time_to_execute=instance.exec_time,
        ))
