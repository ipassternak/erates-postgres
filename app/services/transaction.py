from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.transaction import Transaction, TransactionStatus
import app.services.wallet as wallet_service
import app.services.exchange_rate as exchange_rate_service
from app.schemas.transaction import CreateTransactionSchema, GetTransactionListSchema

def get_list(db: Session, params: GetTransactionListSchema, decoded_token: dict) -> list[Transaction]:
    user_id = decoded_token["sub"]
    query = db.query(Transaction).filter(Transaction.user_id == user_id)
    if params.from_currency:
        query = query.filter(Transaction.from_currency == params.from_currency)
    if params.to_currency:
        query = query.filter(Transaction.to_currency == params.to_currency)
    query = (
        query
        .order_by(Transaction.created_at.desc())
        .offset((params.page - 1) * params.page_size)
        .limit(params.page_size)
    )
    return query.all()

def create_item(db: Session, data: CreateTransactionSchema, decoded_token: dict) -> Transaction:
    user_id = decoded_token["sub"]
    exchange_rate = exchange_rate_service.get_item(db, data.exchange_rate_id)
    from_wallet = wallet_service.get_item(db, data.from_wallet_id, decoded_token)
    if from_wallet.currency != exchange_rate.from_currency:
        raise HTTPException(status_code=400, detail="Invalid base wallet currency")
    to_wallet = wallet_service.get_item(db, data.to_wallet_id, decoded_token)
    if to_wallet.currency != exchange_rate.to_currency:
        raise HTTPException(status_code=400, detail="Invalid target wallet currency")
    withdraw_amount = data.amount / exchange_rate.rate
    deposit_amount = data.amount
    wallet_service.withdraw(db, from_wallet, withdraw_amount)
    wallet_service.deposit(db, to_wallet, deposit_amount)
    new_transaction = Transaction(
        from_wallet_id=data.from_wallet_id,
        to_wallet_id=data.to_wallet_id,
        exchange_rate_id=data.exchange_rate_id,
        from_currency=exchange_rate.from_currency,
        to_currency=exchange_rate.to_currency,
        from_amount=withdraw_amount,
        to_amount=deposit_amount,
        user_id=user_id,
        status=TransactionStatus.COMPLETED,
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction
