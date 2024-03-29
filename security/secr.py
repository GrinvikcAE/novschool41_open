from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from fastapi import HTTPException, Depends, Request

from auth.models import User
from config import JWT_SECRET, ALGORITHM, COOKIE_NAME, ACCESS_TOKEN_EXPIRE_MINUTES

JWT_SECRET = JWT_SECRET
ALGORITHM = ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='user/signin')
COOKIE_NAME = COOKIE_NAME


async def create_access_token(user):
    try:
        payload = {
            "email": user.email,
            'hashed_password': user.hashed_password,
            'is_active': user.is_active
        }
        return jwt.encode(payload, key=JWT_SECRET, algorithm=ALGORITHM)
    except HTTPException as e:
        print(str(e))
        raise e


async def verify_token(token):
    try:
        payload = jwt.decode(token, key=JWT_SECRET, algorithms=ALGORITHM)
        return payload
    except HTTPException as e:
        print(str(e))
        raise e


async def get_password_hash(password):
    return pwd_context.hash(password)


async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def get_current_user_from_token(token: str = Depends(oauth2_scheme)):
    user = await verify_token(token)
    return user


async def get_current_user_from_cookie(request: Request) -> User:
    token = request.cookies.get(COOKIE_NAME)
    if token:
        user = await verify_token(token)
        return user
