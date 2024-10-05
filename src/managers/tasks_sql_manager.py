from abstracts.model_manager import SQLAlchemyBaseModelManager
from models.task import TaskModel, TaskStatuses


class TasksSQLManager(SQLAlchemyBaseModelManager):
    model = TaskModel

    def next_status(self) -> TaskStatuses:
        match self.model.status:
            case TaskStatuses.in_queue:
                return TaskStatuses.run
            case TaskStatuses.run:
                return TaskStatuses.completed
            case _:
                raise ValueError(f"No next status for {self.model.status}")

    async def update(self, instance_id: str, data: dict | None) -> None:
        next_status = self.next_status()
        data.update(status=next_status)
        return await super().update(instance_id, data)
