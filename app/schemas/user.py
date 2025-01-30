from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Схема для пользователя, полученного из БД."""
    pass


class UserCreate(schemas.BaseUserCreate):
    """Схема для создания пользователя."""
    pass


class UserUpdate(schemas.BaseUserUpdate):
    """Схема для обновления пользователя."""
    pass
