from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.schemas.user import RegisterSchema, LoginSchema
from app.security import hash_password, issue_token, verify_password

def register(db: Session, data: RegisterSchema) -> User:
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(data.password)
    new_user = User(
        full_name=data.full_name,
        email=data.email,
        password=hashed_password,
        role=UserRole.USER,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login(db: Session, data: LoginSchema) -> str:
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return issue_token({"sub": user.id, "email": user.email, "role": user.role.value})

def get_user(db: Session, decoded_token: dict) -> User:
    user = db.query(User).filter(User.id == decoded_token["sub"]).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
