from sqlmodel import Session, select
from models.user import User
from fastapi import Request
from fastapi.responses import RedirectResponse
import jwt, os


async def remove_user(request: Request, session: Session):
    try:
        payload = jwt.decode(
            request.session["Authorization"],
            os.getenv("SECRET_KEY"),
            [os.getenv("ALGORITHM")],
        )

    except jwt.InvalidTokenError:
        return RedirectResponse("/login", status_code=401)

    user = session.exec(select(User).where(User.id == payload["id"])).one()

    session.delete(user)
    session.commit()

    del request.session["Authorization"]

    return RedirectResponse("/login", status_code=302)
