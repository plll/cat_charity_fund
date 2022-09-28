from typing import Union

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return project


async def check_project_didnt_have_donations(
        project: CharityProject
):
    if project.invested_amount != 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


async def check_unique_project_name(
    project_name: str,
    session: AsyncSession,
    id: Union[int, None] = None
) -> None:
    project = await charity_project_crud.get_project_by_name(project_name, session)
    if project is not None and project != id:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_isnt_fully_invested(
        project: CharityProject,
        session: AsyncSession
) -> None:
    if project.fully_invested is True:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!',
        )


async def check_update_amount(
        project_investments: int,
        new_amount: int
) -> None:
    if project_investments > new_amount:
        raise HTTPException(
            status_code=400,
            detail='Нельзя'
        )
