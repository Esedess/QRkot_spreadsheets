from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import SPREADSHEETS_URL
from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.logger import logger
from app.core.user import current_superuser
from app.crud.charityproject import charity_project_crud
from app.services import (set_user_permissions, spreadsheets_create,
                          spreadsheets_update_value)

router = APIRouter()


@router.post(
    '/',
    response_model=str,
    dependencies=[Depends(current_superuser)],
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)

):
    """Только для суперюзеров."""
    projects = await charity_project_crud.get_projects_by_completion_rate(
        session,
    )
    spreadsheetid = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheetid, wrapper_services)
    await spreadsheets_update_value(spreadsheetid,
                                    projects,
                                    wrapper_services)
    link = SPREADSHEETS_URL.format(spreadsheetid)
    logger.info(link)
    return link
