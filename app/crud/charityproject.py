from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> list[dict[str, str]]:
        projects = await session.execute(
            select(
                [
                    CharityProject.name,
                    CharityProject.close_date,
                    CharityProject.create_date,
                    CharityProject.description,
                ]).where(
                CharityProject.fully_invested == 1
            )
        )
        projects = [project._asdict() for project in projects.all()]
        for project in projects:
            description = project.pop('description')
            close_date = project.pop('close_date')
            create_date = project.pop('create_date')
            closing_speed = close_date - create_date
            project.update(
                {'closing_speed': closing_speed, 'description': description})
        projects = sorted(projects, key=lambda k: k['closing_speed'])
        return projects


charity_project_crud = CRUDCharityProject(CharityProject)
