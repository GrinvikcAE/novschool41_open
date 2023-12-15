from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict


class OrderCreate(BaseModel):

    last_name: str
    first_name: str
    surname: str
    class_number: str
    email: EmailStr
    birth_date: date


class OrderRead(BaseModel):

    id: int
    last_name: str
    first_name: str
    surname: str
    class_number: str
    email: EmailStr
    birth_date: date
    filename: str
    is_ready: bool
    registered_on: Optional[datetime]
    complete_on: Optional[datetime]
