from typing import Optional

from fastapi_users import schemas
from pydantic import EmailStr


class UserSchema(schemas.BaseUser[int]):

    email: EmailStr
    password: str


class UserCreate(schemas.BaseUserCreate):

    email: EmailStr
    password: str
    role_id: int
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    pass
