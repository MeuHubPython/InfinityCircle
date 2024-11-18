from sqlmodel import Session, select
from models.user import User
from fastapi import Request
from fastapi.templating import Jinja2Templates
from base64 import b64encode
import jwt, os


async def get_card(user_id: int, request: Request, session: Session):
    payload = jwt.decode(
        request.session["Authorization"],
        os.getenv("SECRET_KEY"),
        algorithms=[os.getenv("ALGORITHM")],
    )
    current_user = session.exec(select(User).where(User.id == payload["id"])).one()

    user = session.exec(select(User).where(User.id == user_id)).one()

    return Jinja2Templates(directory="templates").TemplateResponse(
        request=request,
        name="card.html",
        context={"user": user, "current_user": current_user},
    )
