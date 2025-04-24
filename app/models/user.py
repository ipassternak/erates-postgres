from datetime import datetime
import uuid
from app.models.base import Base
from enum import Enum
from sqlalchemy import Column, DateTime, String, Enum as SAEnum

class UserRole(Enum):
    USER = "user"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(length=36), primary_key=True, default=lambda: str(uuid.uuid4()))
    full_name = Column(String(length=64), nullable=False)
    email = Column(String(length=255), unique=True, nullable=False)
    password = Column(String(length=255), nullable=False)
    role: UserRole = Column(SAEnum(UserRole), default=UserRole.USER, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
