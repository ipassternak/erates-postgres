from fastapi import HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from app.models.user import UserRole
from app.security import decode_token

def auth(request: Request) -> dict:
    token = request.cookies.get("token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    decoded_token = decode_token(token)
    return decoded_token

def auth_admin(request: Request) -> dict:
    decoded_token = auth(request)
    if decoded_token["role"] != UserRole.ADMIN.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return decoded_token

templates = Jinja2Templates(directory="public/templates")
