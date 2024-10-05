from .abstracts.model_manager import SQLAlchemyBaseModelManager
from models.task import TaskModel, TaskStatuses


class TasksSQLManager(SQLAlchemyBaseModelManager):
    model = TaskModel

    @staticmethod
    def next_status(current_status) -> TaskStatuses:
        match current_status:
            case TaskStatuses.in_queue:
                return TaskStatuses.run
            case TaskStatuses.run:
                return TaskStatuses.completed
            case _:
                raise ValueError(f"No next status for {current_status}")

    async def update(self, instance_id: str, data: dict | None) -> None:
        instance = await self.get_by_id(instance_id)
        next_status = self.next_status(instance.status)
        data.update(status=next_status)
        return await super().update(instance_id, data)
