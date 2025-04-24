from datetime import datetime
import uuid
from app.models.base import Base, Currency
from sqlalchemy import Column, DateTime, String, ForeignKey, Float, Enum as SAEnum

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(String(length=36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(length=64), nullable=False)
    user_id = Column(String(length=36), ForeignKey("users.id"), nullable=False)
    currency: Currency = Column(SAEnum(Currency), nullable=False)
    balance = Column(Float, default=0.0, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    archived_at = Column(DateTime, nullable=True)
