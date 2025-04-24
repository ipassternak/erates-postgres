from datetime import datetime
from fastapi import HTTPException
from app.models.base import Currency
import uuid
from app.models.wallet import Wallet
from app.schemas.wallet import CreateWalletSchema, GetWalletListSchema, UpdateWalletBalanceSchema, UpdateWalletSchema

def deposit(cursor, wallet: Wallet, amount: float) -> Wallet:
    wallet.balance += amount
    wallet.updated_at = datetime.now()
    cursor.execute(
        """
        UPDATE wallets
        SET balance = %s, updated_at = %s
        WHERE id = %s
        RETURNING id, name, currency, balance, created_at, updated_at
        """,
        (wallet.balance, wallet.updated_at, wallet.id)
    )
    cursor.connection.commit()
    raw_wallet = cursor.fetchone()
    if not raw_wallet:
        raise HTTPException(status_code=400, detail="Failed to deposit")
    wallet = Wallet(
        id=raw_wallet[0],
        name=raw_wallet[1],
        currency=Currency(raw_wallet[2]),
        balance=raw_wallet[3],
        created_at=raw_wallet[4],
        updated_at=raw_wallet[5],
    )
    return wallet

def withdraw(cursor, wallet: Wallet, amount: float) -> Wallet:
    if wallet.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    wallet.balance -= amount
    wallet.updated_at = datetime.now()
    cursor.execute(
        """
        UPDATE wallets
        SET balance = %s, updated_at = %s
        WHERE id = %s
        RETURNING id, name, currency, balance, created_at, updated_at
        """,
        (wallet.balance, wallet.updated_at, wallet.id)
    )
    cursor.connection.commit()
    raw_wallet = cursor.fetchone()
    if not raw_wallet:
        raise HTTPException(status_code=400, detail="Failed to withdraw")
    wallet = Wallet(
        id=raw_wallet[0],
        name=raw_wallet[1],
        currency=Currency(raw_wallet[2]),
        balance=raw_wallet[3],
        created_at=raw_wallet[4],
        updated_at=raw_wallet[5],
    )
    return wallet

def get_list(cursor, params: GetWalletListSchema, decoded_token: dict) -> list[Wallet]:
    user_id = decoded_token["sub"]

    query = """
        SELECT w.id, w.name, w.currency, w.balance, w.created_at, w.updated_at
        FROM wallets w
        WHERE w.user_id = %s
    """
    query_params = [user_id]

    if not params.with_archived:
        query += " AND w.archived_at IS NULL"
    if params.currency:
        query += " AND w.currency = %s"
        query_params.append(params.currency)

    query += " ORDER BY w.created_at DESC LIMIT %s OFFSET %s"
    query_params.append(params.page_size)
    query_params.append((params.page - 1) * params.page_size)

    cursor.execute(query, query_params)
    raw_wallets = cursor.fetchall()

    return [
        Wallet(
            id=raw_wallet[0],
            name=raw_wallet[1],
            currency=Currency(raw_wallet[2]),
            balance=raw_wallet[3],
            created_at=raw_wallet[4],
            updated_at=raw_wallet[5],
        )
        for raw_wallet in raw_wallets
    ]

def get_item(cursor, id: str, decoded_token: dict) -> Wallet:
    user_id = decoded_token["sub"]
    query = """
        SELECT w.id, w.name, w.currency, w.balance, w.created_at, w.updated_at
        FROM wallets w
        WHERE w.id = %s
        AND w.user_id = %s
    """
    query_params = [id, user_id]
    cursor.execute(query, query_params)
    raw_wallet = cursor.fetchone()
    if not raw_wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return Wallet(
        id=raw_wallet[0],
        name=raw_wallet[1],
        currency=Currency(raw_wallet[2]),
        balance=raw_wallet[3],
        created_at=raw_wallet[4],
        updated_at=raw_wallet[5],
    )

def create_item(cursor, data: CreateWalletSchema, decoded_token: dict) -> Wallet:
    user_id = decoded_token["sub"]
    query = """
        INSERT INTO wallets (id, name, user_id, currency, balance, created_at, updated_at)
        VALUES (%s, %s, %s, %s, 0, %s, %s)
        RETURNING id, name, currency, balance, created_at, updated_at
    """
    query_params = [uuid.uuid4(), data.name, user_id, data.currency.value, datetime.now(), datetime.now()]
    cursor.execute(query, query_params)
    cursor.connection.commit()
    raw_wallet = cursor.fetchone()
    if not raw_wallet:
        raise HTTPException(status_code=400, detail="Failed to create wallet")
    return Wallet(
        id=raw_wallet[0],
        name=raw_wallet[1],
        currency=Currency(raw_wallet[2]),
        balance=raw_wallet[3],
        created_at=raw_wallet[4],
        updated_at=raw_wallet[5],
    )

def update_item(cursor, id: str, data: UpdateWalletSchema, decoded_token: dict) -> Wallet:
    user_id = decoded_token["sub"]
    get_query = """
        SELECT w.id, w.name, w.currency, w.balance, w.created_at, w.updated_at
        FROM wallets w
        WHERE w.id = %s
        AND w.user_id = %s
    """
    get_query_params = [id, user_id]
    cursor.execute(get_query, get_query_params)
    raw_wallet = cursor.fetchone()
    if not raw_wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    update_query = """
        UPDATE wallets
        SET name = %s,
            updated_at = %s,
            archived_at = %s
        WHERE id = %s
        RETURNING id, name, currency, balance, created_at, updated_at
    """
    update_query_params = [
        data.name if data.name else raw_wallet[1],
        datetime.now(),
        datetime.now() if data.is_archived else raw_wallet[5],
        id,
    ]
    cursor.execute(update_query, update_query_params)
    cursor.connection.commit()
    updated_raw_wallet = cursor.fetchone()
    if not updated_raw_wallet:
        raise HTTPException(status_code=400, detail="Failed to update wallet")
    return Wallet(
        id=updated_raw_wallet[0],
        name=updated_raw_wallet[1],
        currency=Currency(updated_raw_wallet[2]),
        balance=updated_raw_wallet[3],
        created_at=updated_raw_wallet[4],
        updated_at=updated_raw_wallet[5],
    )

def delete_item(cursor, id: str, decoded_token: dict) -> None:
    user_id = decoded_token["sub"]
    get_query = """
        SELECT w.id, w.name, w.currency, w.balance, w.created_at, w.updated_at
        FROM wallets w
        WHERE w.id = %s
        AND w.user_id = %s
    """
    get_query_params = [id, user_id]
    cursor.execute(get_query, get_query_params)
    raw_wallet = cursor.fetchone()
    if not raw_wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    in_use_query = """
        SELECT t.id
        FROM transactions t
        WHERE t.to_wallet_id = %s OR t.from_wallet_id = %s
    """
    in_use_query_params = [id, id]
    cursor.execute(in_use_query, in_use_query_params)
    in_use = cursor.fetchone()
    if in_use:
        raise HTTPException(status_code=400, detail="Wallet is in use")
    delete_query = """
        DELETE FROM wallets
        WHERE id = %s
    """
    delete_query_params = [id]
    cursor.execute(delete_query, delete_query_params)
    cursor.connection.commit()
    return None

def deposit_item(cursor, id: str, data: UpdateWalletBalanceSchema, decoded_token: dict) -> Wallet:
    user_id = decoded_token["sub"]
    query = """
        SELECT w.id, w.name, w.currency, w.balance, w.created_at, w.updated_at
        FROM wallets w
        WHERE w.id = %s
        AND w.user_id = %s
    """
    query_params = [id, user_id]
    cursor.execute(query, query_params)
    raw_wallet = cursor.fetchone()
    wallet = Wallet(
        id=raw_wallet[0],
        name=raw_wallet[1],
        currency=Currency(raw_wallet[2]),
        balance=raw_wallet[3],
        created_at=raw_wallet[4],
        updated_at=raw_wallet[5],
    )
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    deposit(cursor, wallet, data.amount)
    return wallet

def withdraw_item(cursor, id: str, data: UpdateWalletBalanceSchema, decoded_token: dict) -> Wallet:
    user_id = decoded_token["sub"]
    query = """
        SELECT w.id, w.name, w.currency, w.balance, w.created_at, w.updated_at
        FROM wallets w
        WHERE w.id = %s
        AND w.user_id = %s
    """
    query_params = [id, user_id]
    cursor.execute(query, query_params)
    raw_wallet = cursor.fetchone()
    wallet = Wallet(
        id=raw_wallet[0],
        name=raw_wallet[1],
        currency=Currency(raw_wallet[2]),
        balance=raw_wallet[3],
        created_at=raw_wallet[4],
        updated_at=raw_wallet[5],
    )
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    withdraw(cursor, wallet, data.amount)
    return wallet
