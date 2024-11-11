from fastapi import Request
from fastapi.responses import RedirectResponse
from middlewares.token import remove_token
from fastapi import HTTPException


async def logout_user(request: Request):
    shutdown = await remove_token(request)
    if shutdown == True:
        return RedirectResponse("/", status_code=302)

    return HTTPException(status_code=401, detail="Token not found")
