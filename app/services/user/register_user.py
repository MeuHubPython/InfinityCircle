from models.user import User
from schemas.user.user_register import CreateUser
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlmodel import Session
from datetime import datetime
import bcrypt


async def register_user(request, new_user: CreateUser, session: Session):

    try:
        hashed_password = bcrypt.hashpw(new_user.password.encode(), bcrypt.gensalt())

        user = User(
            name=new_user.name,
            email=new_user.email,
            password=hashed_password,
            profile_image=new_user.profile_image,
            image_format=new_user.image_format,
            created_at=datetime.now().strftime("%D %H:%M"),
        )

        session.add(user)
        session.commit()
        session.refresh(user)

    except Exception as e:
        print(e)
        return Jinja2Templates(directory="templates").TemplateResponse(
            request=request,
            name="register.html",
            context={"email_exists": True},
            status_code=409,
        )

    return RedirectResponse("/login", status_code=302)
