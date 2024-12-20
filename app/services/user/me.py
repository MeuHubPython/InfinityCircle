from sqlmodel import Session, select
from models.user import User
from fastapi import Request
from fastapi.templating import Jinja2Templates
from base64 import b64encode
import jwt, os


async def get_me(request: Request, session: Session):

    token = request.session["Authorization"]
    payload = jwt.decode(
        token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")]
    )
    user = session.exec(select(User).where(User.id == payload["id"])).one()

    return Jinja2Templates(directory="templates").TemplateResponse(
        request=request, name="me.html", context={"user": user}
    )
