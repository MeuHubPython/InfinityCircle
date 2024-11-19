from sqlmodel import Session, select
from fastapi import Request
from models.flow import Flow
from models.user import User
from models.post import Post
from fastapi.responses import RedirectResponse
from datetime import datetime
import jwt, os


async def add_flow(request: Request, post_id: int, session: Session):
    token = request.session["Authorization"]
    payload = jwt.decode(
        token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")]
    )

    user = session.exec(select(User).where(User.id == payload["id"])).one()

    post = session.exec(select(Post).where(Post.id == post_id)).one()

    for flow in user.flows:
        if flow.post_id == post_id:
            return RedirectResponse(f"/connections/{post_id}", status_code=302)

    flow = Flow(
        user_id=user.id,
        post_id=post.id,
        created_at=datetime.now().strftime("%D %H:%M"),
    )
    post.flows.append(flow)
    post.flows_count = len(post.flows)

    user.flows.append(flow)
    user.flows_count = len(user.flows)

    session.add(flow)
    session.add(user)
    session.add(post)
    session.commit()

    return RedirectResponse(f"/connections/{post_id}", status_code=302)
