from datetime import datetime
import uuid
from app.models.base import Base, Currency
from sqlalchemy import Column, DateTime, Float, String, Enum as SAEnum, UniqueConstraint

class ExchangeRate(Base):
    __tablename__ = "exchange_rates"
    
    id = Column(String(length=36), primary_key=True, default=lambda: str(uuid.uuid4()))
    from_currency: Currency = Column(SAEnum(Currency), nullable=False)
    to_currency: Currency = Column(SAEnum(Currency), nullable=False)
    rate = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    __table_args__ = (
        UniqueConstraint('from_currency', 'to_currency', name='exchange_rate_from_to_currency_uk'),
    )
