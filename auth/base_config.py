from fastapi import Request
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport
from fastapi_users.authentication import AuthenticationBackend, JWTStrategy

from .manager import get_user_manager
from config import SECRET_KEY

from .models import User

cookie_transport = CookieTransport(cookie_name='novschool41', cookie_max_age=86400)

SECRET = SECRET_KEY


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=86400)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


async def get_enabled_backends(request: Request):
    if '/pages/search/' in request.url.path or '/orders' in request.url.path:
        return [auth_backend]
    else:
        return []


current_user = fastapi_users.current_user(get_enabled_backends=get_enabled_backends)

