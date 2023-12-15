from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from fastapi import HTTPException, Depends, Request

from auth.models import User

JWT_SECRET = 'gvHfCFPF27sfgzE8bjAY1kinz46Q238ftzkW50t4WMc7eIXhSq'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 3000

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='user/signin')
COOKIE_NAME = "Authorization"


def create_access_token(user):
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


def verify_token(token):
    try:
        payload = jwt.decode(token, key=JWT_SECRET, algorithms=ALGORITHM)
        return payload
    except HTTPException as e:
        print(str(e))
        raise e


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_current_user_from_token(token: str = Depends(oauth2_scheme)):
    user = verify_token(token)
    return user


def get_current_user_from_cookie(request: Request) -> User:
    token = request.cookies.get(COOKIE_NAME)
    if token:
        user = verify_token(token)
        return user
