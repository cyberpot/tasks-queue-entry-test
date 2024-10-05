import fastapi
from fastapi import APIRouter, UploadFile, HTTPException
from starlette import status

from deps.service_dependency import ServiceDependencyType
from routers.core import CoreRoutePath
from entities.response_entities import CreatedTaskResponse, TaskInfoResponse
from services.tasks_processors import process

core_router = APIRouter(tags=["solution-api"])


@core_router.post(
    path=CoreRoutePath.create_task,
    response_model=CreatedTaskResponse,
)
async def create_task(
    response: fastapi.Response
) -> CreatedTaskResponse:
    task_id = await process.delay()
    response.status_code = status.HTTP_201_CREATED
    return CreatedTaskResponse(task_id=task_id)


@core_router.get(
    path=CoreRoutePath.get_task_info,
    response_model=TaskInfoResponse
)
async def get_task_info(
    task_id: str,
    service: ServiceDependencyType,
    response: fastapi.Response,
) -> TaskInfoResponse:
    result = await service.get_task_info(task_id)
    if not result:
        raise HTTPException(
            detail="Not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return TaskInfoResponse(
        **(await service.get_task_info(task_id))
    )
