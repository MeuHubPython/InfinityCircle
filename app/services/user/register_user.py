from models.user import User
from schemas.user.user_register import CreateUser
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlmodel import Session
from datetime import datetime
from base64 import b64encode
import bcrypt


async def register_user(
    request, new_user: CreateUser, session: Session, profile_image: bytes | None = None
):

    try:
        hashed_password = bcrypt.hashpw(new_user.password.encode(), bcrypt.gensalt())
        image = await profile_image.read()
        image_encoded = b64encode(image).decode("utf-8")
        user_image = "data:" + profile_image.content_type + ";base64," + image_encoded

        user = User(
            name=new_user.name,
            email=new_user.email,
            password=hashed_password,
            image_encoded=user_image,
            created_at=datetime.now().strftime("%d/%m/%y %H:%M"),
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
