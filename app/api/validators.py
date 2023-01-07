from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import (FULL_AMOUNT_BEFORE_EDIT_ERR,
                                NAME_DUPLICATE_ERR, PROJECT_EXISTS_ERR,
                                PROJECT_INVESTED_BEFORE_DELETE_ERR,
                                PROJECT_NOT_CLOSED_ERR)
from app.crud.charityproject import charity_project_crud
from app.models import CharityProject


async def check_project_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session)

    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=NAME_DUPLICATE_ERR
        )


async def check_charity_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=PROJECT_EXISTS_ERR
        )
    return project


def check_charity_project_not_closed(
        project: CharityProject,
) -> None:
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_NOT_CLOSED_ERR
        )


def check_charity_project_full_amount_before_edit(
        new_full_amount: int,
        project: CharityProject,
) -> None:
    if project.invested_amount > new_full_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=FULL_AMOUNT_BEFORE_EDIT_ERR
        )


def check_charity_project_invested_before_delete(
        project: CharityProject,
) -> None:
    if project.invested_amount != 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_INVESTED_BEFORE_DELETE_ERR
        )
