from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CoreRoutePath:
    create_task = "/tasks/create"
    get_task_info = "/tasks/{task_id}"
