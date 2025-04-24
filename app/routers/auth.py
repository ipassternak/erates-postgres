import os
from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import auth
from app.schemas.user import LoginSchema, RegisterSchema
import app.services.user as user_service

TOKEN_EXPIRE_MINUTES = float(os.getenv("TOKEN_EXPIRE_MINUTES", "60"))

auth_router = APIRouter(
    tags=["Auth"],
    prefix="/api/auth",
)

@auth_router.post("/register")
def register(
    data: RegisterSchema = Body(),
    db: Session = Depends(get_db)
):
    user_service.register(db, data)
    return JSONResponse(content={"status": "success"}, status_code=201)

@auth_router.post("/login")
def login(
    data: LoginSchema = Body(),
    db: Session = Depends(get_db)
):
    token = user_service.login(db, data)
    response = JSONResponse(content={"status": "success"}, status_code=200)
    response.set_cookie(
        key="token",
        value=token,
        httponly=True,
        path="/",
        samesite="Lax",
        secure=False,
        max_age=TOKEN_EXPIRE_MINUTES * 60,
    )
    return response

@auth_router.get("/me")
def me(
    db: Session = Depends(get_db),
    decoded_token: dict = Depends(auth)
):
    user = user_service.get_user(db, decoded_token) 
    user = {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "role": user.role.value,
        "created_at": user.created_at.isoformat(),
        "updated_at": user.updated_at.isoformat(),
    }
    return JSONResponse(content={"status": "success", "item": user}, status_code=200)
