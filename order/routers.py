from datetime import date
from fastapi import APIRouter, Depends, Form
from fastapi.responses import RedirectResponse
from pydantic import EmailStr
from typing import Optional
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from .models import order
from security.secr import get_current_user_from_cookie


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.get('',  dependencies=[Depends(get_current_user_from_cookie)])
async def get_orders(offset: int = 0, limit: int = 100, session: AsyncSession = Depends(get_async_session)):
    query = select(order).offset(offset).limit(offset+limit)
    result = await session.execute(query)
    return result.mappings().all()


@router.get('/{last_name_in_orders}', dependencies=[Depends(get_current_user_from_cookie)])
async def get_specific_orders(last_name_in_orders: str, session: AsyncSession = Depends(get_async_session)):
    query = select(order).where(order.c.last_name == last_name_in_orders)
    result = await session.execute(query)
    return result.mappings().all()


@router.post('/add_order')
async def add_order(last_name: str = Form(max_length=50),
                    first_name: str = Form(max_length=50),
                    surname: str = Form(max_length=50),
                    class_number: str = Form(max_length=5),
                    email: Optional[EmailStr] = Form(max_length=50, default=''),
                    birth_date: date = Form(),
                    session: AsyncSession = Depends(get_async_session)):
    result = {'last_name': last_name,
              'first_name': first_name,
              'surname': surname,
              'class_number': class_number,
              'email': email,
              'birth_date': birth_date,
              }
    stmt = insert(order).values(**result)
    await session.execute(stmt)
    await session.commit()
    return RedirectResponse('/pages/home', status_code=302)


@router.post('/del_order/{order_id}', dependencies=[Depends(get_current_user_from_cookie)])
async def del_order_by_id(order_id: int, session: AsyncSession = Depends(get_async_session)):
    query = delete(order).where(order.c.id == order_id)
    await session.execute(query)
    await session.commit()
    return RedirectResponse('/pages/search', status_code=302)
