from typing import Annotated
from repository.user import UserRepository
from security.secr import verify_password, create_access_token, get_password_hash, verify_token
from auth.models import User
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse, Response
from security.secr import COOKIE_NAME

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.post('/login')
async def login(
        response: Response,
        username: Annotated[str, Form()],
        password: Annotated[str, Form()],
        db: AsyncSession = Depends(get_async_session)):
    userRepository = UserRepository(db)
    db_user = await userRepository.get_user_by_email(username)

    if not db_user:
        return "email or password is not valid"
    if await verify_password(password, db_user['hashed_password']):
        token = await create_access_token(db_user)
        response = RedirectResponse(url='/pages/search')
        response.set_cookie(key=COOKIE_NAME, value=token, httponly=True, expires=3600)
        return response
    else:
        raise HTTPException(status_code=401, detail='Credentials not correct')


@router.post('/logout')
async def logout(response: Response):
    response = RedirectResponse(url='/pages/home')
    response.delete_cookie(key=COOKIE_NAME)
    return response


@router.post('/signup')
async def signup(
        response: Response,
        username: Annotated[str, Form()],
        password: Annotated[str, Form()],
        db: AsyncSession = Depends(get_async_session)):
    userRepository = UserRepository(db)

    signup = User(email=username, hashed_password=get_password_hash(password))
    success = await userRepository.create_user(signup)
    if success:
        return "user created successfully"
    else:
        raise HTTPException(status_code=401, detail='Credentials not correct')


@router.get('/verify/{token}')
async def verify_user(token, db: AsyncSession = Depends(get_async_session)):
    userRepository = UserRepository(db)
    payload = await verify_token(token)
    email = payload.get('email')
    db_user = await userRepository.get_user_by_email(email)
    if not email:
        raise HTTPException(status_code=401, detail='Credentials not correct')
    if db_user.is_active:
        return "User already active"
    db_user.is_active = True
    await db.commit()
    response = RedirectResponse(url='/auth/login')
    return response
