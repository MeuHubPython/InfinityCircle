from fastapi import APIRouter, Form, Depends, Request
from fastapi.responses import HTMLResponse
from database.init_db import get_session
from sqlmodel import Session
from schemas.user.user_login import LoginSubmit
from services.user.login_user import login_user
from services.user.register_user import register_user
from fastapi.templating import Jinja2Templates
from schemas.user.user_register import CreateUser


router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
async def render_login(request: Request):
    return Jinja2Templates(directory="templates").TemplateResponse(
        request=request, name="login.html"
    )


@router.post("/login/submit", response_model=LoginSubmit)
async def submit_login(
    request: Request,
    email: str = Form(),
    password: str = Form(),
    session: Session = Depends(get_session),
):
    return await login_user(request, email, password, session)


@router.get("/register")
async def render_register(request: Request):
    return Jinja2Templates(directory="templates").TemplateResponse(
        request=request, name="register.html"
    )


@router.post("/register")
async def submit_register(
    request: Request,
    name: str = Form(),
    email: str = Form(),
    password: str = Form(),
    session: Session = Depends(get_session),
):
    created_user = CreateUser(name=name, email=email, password=password)
    return await register_user(request, created_user, session)
