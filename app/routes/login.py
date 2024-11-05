from fastapi import APIRouter, Form, Depends, Request
from fastapi.responses import HTMLResponse
from database.init_db import get_session
from sqlmodel import Session
from schemas.user.user_login import LoginSubmit
from services.user.login_user import login_user
from fastapi.templating import Jinja2Templates


router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return Jinja2Templates(directory="templates").TemplateResponse(
        request=request, name="login.html"
    )


@router.post("/login/submit", response_model=LoginSubmit)
async def test(
    request: Request,
    email: str = Form(),
    password: str = Form(),
    session: Session = Depends(get_session),
):
    return await login_user(request, email, password, session)


@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return Jinja2Templates(directory="templates").TemplateResponse(
        request=request, name="register.html"
    )
