from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.constants import (FULL_AMOUNT_ERROR, PROJECT_DOESNT_EXIST,
                               PROJECT_HAS_DONATIONS, PROJECT_IS_CLOSED,
                               PROJECT_NAME_ALREADY_EXISTS)
from app.crud import charity_project_crud
from app.models import CharityProject


async def check_charity_project_name_duplicate(
        project_name: str,
        session: AsyncSession
):
    charity_project_id = await charity_project_crud.get_id_by_name(
        project_name,
        session
    )
    if charity_project_id is not None:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            PROJECT_NAME_ALREADY_EXISTS
        )


async def check_charity_project_exists(
        project_id: int,
        session: AsyncSession
) -> CharityProject:
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=PROJECT_DOESNT_EXIST,
        )
    if charity_project.close_date is not None:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            PROJECT_IS_CLOSED
        )
    return charity_project


async def check_full_amount_value(
        full_amount: int,
        charity_project: CharityProject,
        session: AsyncSession
) -> CharityProject:
    if full_amount < charity_project.invested_amount:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            FULL_AMOUNT_ERROR
        )
    if full_amount == charity_project.invested_amount:
        charity_project = await charity_project_crud.close_obj(
            charity_project, session
        )
    return charity_project


async def check_project_has_donations(
        charity_project: CharityProject,
):
    if charity_project.invested_amount > 0:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            PROJECT_HAS_DONATIONS
        )
