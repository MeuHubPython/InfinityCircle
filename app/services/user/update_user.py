from models.user import User
from sqlmodel import Session, select
from schemas.user.user_register import CreateUser
from fastapi import HTTPException
import bcrypt


async def update_user(user_email: str, user: CreateUser, session: Session):

    try:
        user_db = session.exec(select(User).where(User.email == user_email)).one()
    except Exception:
        raise HTTPException(status_code=404, detail="User not found")

    user_db.name = user.name
    user_db.email = user.email
    user_db.password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())

    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    return user_db
