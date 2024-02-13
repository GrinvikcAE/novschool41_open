from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, EmailStr


class OrderCreate(BaseModel):

    last_name: str
    first_name: str
    surname: str
    class_number: str
    email: Optional[EmailStr]
    birth_date: date


class OrderRead(BaseModel):

    id: int
    last_name: str
    first_name: str
    surname: str
    class_number: str
    email: Optional[EmailStr]
    birth_date: date
    registered_on_utc: Optional[datetime]
    registered_on_now: Optional[datetime]
