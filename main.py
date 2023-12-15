import uvicorn
from fastapi import FastAPI, status
from pydantic import ValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from auth.base_config import fastapi_users, auth_backend
from auth.models import user, role
from auth.schemas import UserSchema, UserCreate
from auth.routers import router as router_auth
from order.routers import router as router_order
from pages.routers import router as pages_router


from database import engine
from fastapi_users.password import PasswordHelper
from config import EMAIL, PASSWD
from security.secr import get_password_hash


app = FastAPI(
    title="NovSchool41"
)


@app.on_event("startup")
async def create_admin_user():
    try:
        async with engine.begin() as conn:
            roles = [{'id': 1, 'name': 'admin', 'permissions': ['GET', 'POST', 'DELETE', 'UPDATE']},
                     {'id': 2, 'name': 'user', 'permissions': ['GET', 'POST']}]
            try:
                await conn.execute(role.insert(), roles)
            except Exception as e:
                print(e)
        await engine.dispose()

        async with engine.begin() as conn:
            try:
                admin = {
                    "email": EMAIL,
                    "hashed_password": get_password_hash(PASSWD),
                    "is_active": True,
                    "is_superuser": True,
                    "is_verified": True,
                    "role_id": 1
                }
                await conn.execute(user.insert(), admin)
            except Exception as e:
                print(e)
        await engine.dispose()

    except Exception as e:
        print(e)
    pass


app.mount('/static', StaticFiles(directory='static'), name='static')


origins = [
    'http://localhost:8000',
    'https://localhost:8000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Access-Control-Allow-Headers", "Access-Control-Allow-Methods",
                   "Authorization", "Set-Cookie", "Cross-Origin"]
)


@app.exception_handler(ValidationError)
async def validation_exception_handler(exc: ValidationError):
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        content=jsonable_encoder({'detail': exc.errors()}))


app.include_router(pages_router)
app.include_router(router_order)
app.include_router(router_auth)


app.include_router(
    fastapi_users.get_auth_router(auth_backend, requires_verification=False),
    prefix="/auth/jwt",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserSchema, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)


@app.get("/", tags=['Main'])
async def root():
    # try:
    return {"Hello": "World"}
    # except Exception as e:
    #     raise HTTPException(status_code=404, detail={'status': 'error',
    #                                                  'message': e,
    #                                                  'details': None})

# if __name__ == '__main__':
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
