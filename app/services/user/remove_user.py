from sqlmodel import Session, select
from models.user import User
from fastapi import HTTPException


async def remove_user(user_email: str, session: Session):
    try:
        user = session.exec(select(User).where(User.email == user_email)).one()
    except Exception:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(user)
    session.commit()

    return {"message": "User deleted successfully"}
