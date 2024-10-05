from typing import Annotated, TypeAlias

import fastapi.params
from sqlalchemy.ext.asyncio import AsyncSession

from managers.tasks_sql_manager import TasksSQLManager
from models.config import get_db_session
from services.tasks_service import TasksService


def _service_dependency(
    session: Annotated[
        AsyncSession,
        fastapi.params.Depends(get_db_session)
    ],
) -> TasksService:
    return TasksService(sql_manager=TasksSQLManager(session=session))


ServiceDependency = fastapi.params.Depends(_service_dependency)
ServiceDependencyType: TypeAlias = Annotated[
    TasksService,
    ServiceDependency
]
