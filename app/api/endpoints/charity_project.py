from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_exists,
                                check_charity_project_name_duplicate,
                                check_full_amount_value,
                                check_project_has_donations)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.schemas import (CharityProjectCreate, CharityProjectDB,
                         CharityProjectUpdate)
from app.services.donation import distribute_all_donations

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)])
async def create_charity_project(
    data: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперпользователей.
    Создаёт благотворительный проект.
    """
    await check_charity_project_name_duplicate(data.name, session)
    charity_project = await charity_project_crud.create(data, session)
    return await distribute_all_donations(charity_project, session)


@router.get(
    '/',
    response_model=list[CharityProjectDB])
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список всех проектов."""
    return await charity_project_crud.get_all(session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)])
async def update_charity_project(
    data: CharityProjectUpdate,
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Редактирует проект. Только для суперюзеров.
    Закрытый проект нельзя редактировать;
    нельзя установить требуемую сумму меньше уже вложенной.
    """

    charity_project = await check_charity_project_exists(project_id, session)
    if data.name:
        await check_charity_project_name_duplicate(data.name, session)
    if data.full_amount is not None:
        charity_project = await check_full_amount_value(
            data.full_amount, charity_project, session
        )
    return await charity_project_crud.update(
        charity_project, data, session
    )


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)])
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.
    Удаляет проект. Нельзя удалить проект, в который уже были
    инвестированы средства, его можно только закрыть.
    """
    charity_project = await check_charity_project_exists(project_id, session)
    await check_project_has_donations(charity_project)
    await charity_project_crud.remove(charity_project, session)
    return charity_project
