from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from auth.models import user, role
from auth.routers import router as router_auth
from order.routers import router as router_order
from pages.routers import router as pages_router


from database import engine
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
                    "hashed_password": await get_password_hash(PASSWD),
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
    'https://127.0.0.1:8000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    max_age=10,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Content-Type", "Access-Control-Allow-Headers", "Access-Control-Allow-Methods",
                   "Authorization", "Set-Cookie", "Cross-Origin", 'Access-Control-Request-Method']
)


app.include_router(pages_router)
app.include_router(router_order)
app.include_router(router_auth)


@app.get("/", tags=['Main'])
async def root():
    return RedirectResponse('/pages/home', status_code=302)
