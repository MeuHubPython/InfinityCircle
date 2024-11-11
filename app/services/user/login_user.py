from models.user import User
from sqlmodel import Session, select
from fastapi import Form, Request
from fastapi.templating import Jinja2Templates
from middlewares.token import create_token
import bcrypt


async def login_user(
    request: Request,
    email: str = Form(),
    password: str = Form(),
    session: Session = Session,
):
    try:
        user = session.exec(select(User).where(User.email == email)).one()
    except Exception:
        return Jinja2Templates(directory="templates").TemplateResponse(
            request=request,
            name="login.html",
            context={"wrong": True},
            status_code=404,
        )

    if not bcrypt.checkpw(password.encode(), user.password):
        return Jinja2Templates(directory="templates").TemplateResponse(
            request=request,
            name="login.html",
            context={"wrong": True},
            status_code=404,
        )

    token = await create_token(
        {"user": user.name, "email": user.email, "id": user.id}, request
    )
    return {"message": "Login successful", "email": user.email}
