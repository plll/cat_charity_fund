from fastapi import APIRouter, Depends
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.models import User
from app.crud.donation import donation_crud
from app.schemas.donation import (
    DonationDB, DonationCreate
)
from app.api.validators import check_project_exists, check_project_didnt_have_donations
from app.core.user import current_superuser, current_user


router = APIRouter() 


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    response_model_exclude={"close_date", "fully_invested",
                           "user_id", "invested_amount"}
)
async def create_new_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Только для суперюзеров."""
    setattr(donation, 'user_id', user.id)
    donation = await donation_crud.create(donation, session)
    return donation


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.""" 
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude={"close_date", "fully_invested",
                           "user_id", "invested_amount"}
)
async def get_my_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    all_donations = await donation_crud.get_my_donations(user.id, session)
    return all_donations