from typing import Annotated

from fastapi import Depends, APIRouter
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from entities.response_entities import HealthCheckResponse
from models.config import get_db_session


util_router = APIRouter(tags=["utils"])


@util_router.get(
    path="/healthcheck",
    response_model=HealthCheckResponse
)
async def healthcheck(
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> HealthCheckResponse:
    await session.execute(text("SELECT 1"))
    return HealthCheckResponse()
