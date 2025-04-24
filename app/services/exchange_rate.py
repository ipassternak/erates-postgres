from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.exchange_rate import ExchangeRate
from app.schemas.exchange_rate import CreateExchangeRateSchema, GetExchangeRateListSchema, UpdateExchangeRateSchema

def get_list(db: Session, params: GetExchangeRateListSchema) -> list[ExchangeRate]:
    query = db.query(ExchangeRate)
    if params.from_currency:
        query = query.filter(ExchangeRate.from_currency == params.from_currency)
    if params.to_currency:
        query = query.filter(ExchangeRate.to_currency == params.to_currency)
    query = query.order_by(ExchangeRate.updated_at.desc())
    query = query.offset((params.page - 1) * params.page_size).limit(params.page_size)
    return query.all()

def get_item(db: Session, id: str) -> ExchangeRate:
    exchange_rate = db.query(ExchangeRate).filter(ExchangeRate.id == id).first()
    if not exchange_rate:
        raise HTTPException(status_code=404, detail="Exchange rate not found")
    return exchange_rate

def create_item(db: Session, data: CreateExchangeRateSchema) -> ExchangeRate:
    if data.from_currency == data.to_currency:
        raise HTTPException(status_code=400, detail="From and to currencies cannot be the same")
    existing_rate = db.query(ExchangeRate).filter(
        ExchangeRate.from_currency == data.from_currency,
        ExchangeRate.to_currency == data.to_currency
    ).first()
    if existing_rate:
        raise HTTPException(status_code=400, detail="Exchange rate already exists")
    new_rate = ExchangeRate(
        from_currency=data.from_currency,
        to_currency=data.to_currency,
        rate=data.rate
    )
    db.add(new_rate)
    db.commit()
    db.refresh(new_rate)
    return new_rate

def update_item(db: Session, id: str, data: UpdateExchangeRateSchema) -> ExchangeRate:
    exchange_rate = db.query(ExchangeRate).filter(ExchangeRate.id == id).first()
    if not exchange_rate:
        raise HTTPException(status_code=404, detail="Exchange rate not found")
    exchange_rate.rate = data.rate
    db.commit()
    db.refresh(exchange_rate)
    return exchange_rate

def delete_item(db: Session, id: str) -> None:
    exchange_rate = db.query(ExchangeRate).filter(ExchangeRate.id == id).first()
    if not exchange_rate:
        raise HTTPException(status_code=404, detail="Exchange rate not found")
    db.delete(exchange_rate)
    db.commit()
    return None
