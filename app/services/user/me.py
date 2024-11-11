from sqlmodel import Session, select
from models.user import User
from fastapi import Request
import jwt, os


async def get_me(request: Request, session: Session):
    token = request.session["Authorization"]
    payload = jwt.decode(
        token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")]
    )
    user = session.exec(select(User).where(User.id == payload["id"])).one()
    return {"user": user.name, "email": user.email}
