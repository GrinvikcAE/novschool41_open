from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from auth.models import User

from order.routers import get_specific_orders, get_orders
from security.secr import get_current_user_from_cookie

router = APIRouter(
    prefix='/pages',
    tags=['Pages']
)

fastapi_users_proxy_router = APIRouter()


templates = Jinja2Templates(directory='templates')


@router.api_route('/home', response_class=HTMLResponse, methods=['GET', 'POST'])
def get_home_page(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})


@router.api_route('/search', response_class=HTMLResponse, methods=['GET', 'POST'])
def get_search_page(request: Request, orders=Depends(get_orders), user: User = Depends(get_current_user_from_cookie)):
    if user is None:
        return get_home_page(request)
    else:
        return templates.TemplateResponse('search.html', {'request': request, 'orders': orders})


@router.get('/search/{last_name_in_orders}', response_class=HTMLResponse)
def get_search_page(request: Request, orders=Depends(get_specific_orders),
                    user: User = Depends(get_current_user_from_cookie)):
    if user is None:
        return get_home_page(request)
    else:
        return templates.TemplateResponse('search.html', {'request': request, 'orders': orders})


@router.get('/404NotFound', response_class=HTMLResponse)
def get_base_page(request: Request):
    return templates.TemplateResponse('page404.html', {'request': request})


