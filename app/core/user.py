from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import (BaseUserManager, FastAPIUsers, IntegerIDMixin,
                           InvalidPasswordException)
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.constants import (JWT_LEFITIME_SECONDS, PASSWORD_EMAIL_ERROR,
                                PASSWORD_LENGTH_ERROR, PASSWORD_MIN_LENGTH,
                                TOKEN_URL, USER_HAS_REGISTERED)
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """Возвращает генератор пользователя из БД."""
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl=TOKEN_URL)


def get_jwt_strategy() -> JWTStrategy:
    """Возвращает JWT стратегию для FastAPI Users."""
    return JWTStrategy(
        secret=settings.secret,
        lifetime_seconds=JWT_LEFITIME_SECONDS
    )


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """Менеджер для User."""
    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        if len(password) < PASSWORD_MIN_LENGTH:
            raise InvalidPasswordException(
                reason=PASSWORD_LENGTH_ERROR
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason=PASSWORD_EMAIL_ERROR
            )

    async def on_after_register(
            self, user: User, request: Optional[Request] = None
    ):
        print(USER_HAS_REGISTERED.format(user.email))


async def get_user_manager(user_db=Depends(get_user_db)):
    """Возвращает генератор менеджера"""
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
