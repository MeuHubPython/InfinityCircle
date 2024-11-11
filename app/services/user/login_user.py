from models.user import User
from sqlmodel import Session, select
from fastapi import Form, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from middlewares.token import create_token
import bcrypt, jwt, os


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

    token = await create_token({"id": user.id}, request)
    return RedirectResponse("/posts/all_posts", status_code=302)


async def user_already_authenticated(request: Request):
    try:
        token = request.session["Authorization"]

    except KeyError:
        return Jinja2Templates(directory="templates").TemplateResponse(
            request=request, name="login.html", status_code=302
        )

    try:
        decoded_token = jwt.decode(
            token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")]
        )
    except jwt.InvalidTokenError:
        return Jinja2Templates(directory="templates").TemplateResponse(
            request=request, name="login.html", status_code=302
        )
    return RedirectResponse("/posts/all_posts", status_code=302)
