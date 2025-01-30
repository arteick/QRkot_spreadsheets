from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud, donation_crud
from app.models import CharityProject, Donation


async def distribute_donation(
        donation: Donation,
        session: AsyncSession
) -> Donation:
    """
    Распределяет сумму пожертвования между проектами
    при создании пожертвования.
    """
    charity_projects = await charity_project_crud.get_partially_donated(
        CharityProject, session
    )
    if not charity_projects:
        return donation
    for charity_project in charity_projects:
        amount_to_add = min(
            donation.full_amount,
            charity_project.full_amount -
            charity_project.invested_amount
        )
        charity_project.invested_amount += amount_to_add
        if charity_project.full_amount == charity_project.invested_amount:
            charity_project = await charity_project_crud.close_obj(
                charity_project, session
            )
        donation.invested_amount += amount_to_add
        if donation.full_amount == donation.invested_amount:
            donation = await donation_crud.close_obj(
                donation, session
            )
            break
    return await donation_crud.commit_and_refresh(donation, session)


async def distribute_all_donations(
        charity_project: CharityProject,
        session: AsyncSession
) -> AsyncSession:
    """Распределяет пожертвования при создании нового проекта."""
    donations = await donation_crud.get_partially_donated(
        Donation, session
    )
    if not donations:
        return charity_project
    for donation in donations:
        amount_to_add = min(
            donation.full_amount,
            charity_project.full_amount -
            charity_project.invested_amount
        )
        donation.invested_amount += amount_to_add
        if donation.full_amount == donation.invested_amount:
            donation = await donation_crud.close_obj(
                donation, session
            )
        charity_project.invested_amount += amount_to_add
        if charity_project.full_amount == charity_project.invested_amount:
            charity_project = await charity_project_crud.close_obj(
                charity_project, session
            )
            break
    return await charity_project_crud.commit_and_refresh(
        charity_project, session
    )
