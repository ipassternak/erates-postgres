from datetime import datetime
import uuid
from app.models.base import Base, Currency
from enum import Enum
from sqlalchemy import Column, DateTime, String, Enum as SAEnum, ForeignKey, Float

class TransactionStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(String(length=36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(length=36), ForeignKey("users.id"), nullable=False)
    from_currency: Currency = Column(SAEnum(Currency), nullable=False)
    to_currency: Currency = Column(SAEnum(Currency), nullable=False)
    from_wallet_id = Column(String(length=36), ForeignKey("wallets.id"), nullable=False)
    to_wallet_id = Column(String(length=36), ForeignKey("wallets.id"), nullable=False)
    exchange_rate_id = Column(String(length=36), ForeignKey("exchange_rates.id"), nullable=False)
    from_amount = Column(Float, nullable=False)
    to_amount = Column(Float, nullable=False)
    status: TransactionStatus = Column(SAEnum(TransactionStatus), default=TransactionStatus.PENDING, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
