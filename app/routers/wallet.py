from fastapi import APIRouter, Body, Depends, Query, Path, Request
from fastapi.responses import JSONResponse
from app.database import get_cursor
from app.dependencies import auth, templates
from app.schemas.wallet import CreateWalletSchema, GetWalletListSchema, UpdateWalletBalanceSchema, UpdateWalletSchema
import app.services.wallet as wallet_service

wallet_router = APIRouter(
    tags=["Wallets"],
    prefix="/api/wallets",
)

@wallet_router.get("/list")
def get_list(
    request: Request,
    params: GetWalletListSchema = Query(),
    cursor = Depends(get_cursor),
    decoded_token: dict = Depends(auth)
):
    wallets = wallet_service.get_list(cursor, params, decoded_token)
    return templates.TemplateResponse("wallet/list.html", {
        "request": request,
        "wallets": list(map(lambda wallet: {
            "id": wallet.id,
            "name": wallet.name,
            "currency": wallet.currency.value,
            "balance": wallet.balance,
            "created_at": wallet.created_at.strftime("%d/%m/%Y %H:%M"),
            "updated_at": wallet.updated_at.strftime("%d/%m/%Y %H:%M"),
        }, wallets)),
    })

@wallet_router.get("/reference")
def get_reference(
    params: GetWalletListSchema = Query(),
    cursor = Depends(get_cursor),
    decoded_token: dict = Depends(auth)
):
    wallets = wallet_service.get_list(cursor, params, decoded_token)
    return JSONResponse(content={
        "wallets": list(map(lambda wallet: {
            "id": wallet.id,
            "name": wallet.name,
            "currency": wallet.currency.value,
            "balance": wallet.balance,
            "created_at": wallet.created_at.isoformat(),
            "updated_at": wallet.updated_at.isoformat(),
        }, wallets)),
    })

@wallet_router.get("/item/{id}")
def get_item(
    id: str = Path(description="Wallet ID"),
    cursor = Depends(get_cursor),
    decoded_token: dict = Depends(auth)
):
    wallet = wallet_service.get_item(cursor, id, decoded_token)
    wallet = {
        "id": wallet.id,
        "name": wallet.name,
        "currency": wallet.currency.value,
        "balance": wallet.balance,
        "created_at": wallet.created_at.isoformat(),
        "updated_at": wallet.updated_at.isoformat(),
    }
    return JSONResponse(content={"item": wallet})

@wallet_router.post("/item")
def create_item(
    data: CreateWalletSchema = Body(),
    cursor = Depends(get_cursor),
    decoded_token: dict = Depends(auth)
):
    wallet_service.create_item(cursor, data, decoded_token)
    return JSONResponse(content={"status": "success"}, status_code=201)

@wallet_router.put("/item/{id}")
def update_item(
    id: str = Path(description="Wallet ID"),
    data: UpdateWalletSchema = Body(),
    cursor = Depends(get_cursor),
    decoded_token: dict = Depends(auth)
):
    wallet_service.update_item(cursor, id, data, decoded_token)
    return JSONResponse(content={"status": "success"})

@wallet_router.delete("/item/{id}")
def delete_item(
    id: str = Path(description="Wallet ID"),
    cursor = Depends(get_cursor),
    decoded_token: dict = Depends(auth)
):
    wallet_service.delete_item(cursor, id, decoded_token)
    return JSONResponse(content={"status": "success"}, status_code=204)

@wallet_router.post("/item/{id}/deposit")
def deposit_item(
    id: str = Path(description="Wallet ID"),
    data: UpdateWalletBalanceSchema = Body(),
    cursor = Depends(get_cursor),
    decoded_token: dict = Depends(auth)
):
    wallet_service.deposit_item(cursor, id, data, decoded_token)
    return JSONResponse(content={"status": "success"})

@wallet_router.post("/item/{id}/withdraw")
def withdraw_item(
    id: str = Path(description="Wallet ID"),
    data: UpdateWalletBalanceSchema = Body(),
    cursor = Depends(get_cursor),
    decoded_token: dict = Depends(auth)
):
    wallet_service.withdraw_item(cursor, id, data, decoded_token)
    return JSONResponse(content={"status": "success"})
