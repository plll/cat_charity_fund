from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.api.validators import (check_project_exists,
                                check_project_didnt_have_donations,
                                check_unique_project_name,
                                check_project_isnt_fully_invested,
                                check_update_amount)
from app.core.user import current_superuser


router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_unique_project_name(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project, session)
    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    project = await check_project_exists(project_id, session)
    await check_project_didnt_have_donations(project)
    project = await charity_project_crud.remove(project, session)
    return project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_meeting_room(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    project = await check_project_exists(
        project_id, session
    )
    await check_project_isnt_fully_invested(project, session)
    if obj_in.full_amount is not None:
        await check_update_amount(project.invested_amount, obj_in.full_amount)
    if obj_in.name is not None:
        await check_unique_project_name(obj_in.name, session, project_id)
    project = await charity_project_crud.update(
        project, obj_in, session
    )
    return project