from fastapi import APIRouter, Body, Depends, Query, Path, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import auth_admin, templates
from app.schemas.exchange_rate import CreateExchangeRateSchema, GetExchangeRateListSchema, UpdateExchangeRateSchema
import app.services.exchange_rate as exchange_rate_service

exchange_rate_router = APIRouter(
    tags=["Exchange Rate"],
    prefix="/api/exchange-rate",
)

@exchange_rate_router.get("/list")
def get_list(
    request: Request,
    params: GetExchangeRateListSchema = Query(),
    db: Session = Depends(get_db),
):
    exchange_rates = exchange_rate_service.get_list(db, params)
    return templates.TemplateResponse("exchange-rate/list.html", {
        "request": request,
        "exchange_rates": list(map(lambda exchange_rate: {
            "id": exchange_rate.id,
            "from_currency": exchange_rate.from_currency.value,
            "to_currency": exchange_rate.to_currency.value,
            "rate": exchange_rate.rate,
            "created_at": exchange_rate.created_at.strftime("%d/%m/%Y %H:%M"),
            "updated_at": exchange_rate.updated_at.strftime("%d/%m/%Y %H:%M"),
        }, exchange_rates)),
    })

@exchange_rate_router.get("/reference")
def get_reference(
    params: GetExchangeRateListSchema = Query(),
    db: Session = Depends(get_db),
):
    exchange_rates = exchange_rate_service.get_list(db, params)
    return JSONResponse(content={
        "exchange_rates": list(map(lambda exchange_rate: {
            "id": exchange_rate.id,
            "from_currency": exchange_rate.from_currency.value,
            "to_currency": exchange_rate.to_currency.value,
            "rate": exchange_rate.rate,
            "created_at": exchange_rate.created_at.isoformat(),
            "updated_at": exchange_rate.updated_at.isoformat(),
        }, exchange_rates)),
    })

@exchange_rate_router.get("/item/{id}")
def get_item(
    id: str = Path(description="Exchange rate ID"),
    db: Session = Depends(get_db),
):
    exchange_rate = exchange_rate_service.get_item(db, id)
    exchange_rate = {
        "id": exchange_rate.id,
        "from_currency": exchange_rate.from_currency.value,
        "to_currency": exchange_rate.to_currency.value,
        "rate": exchange_rate.rate,
        "created_at": exchange_rate.created_at.isoformat(),
        "updated_at": exchange_rate.updated_at.isoformat(),
    }
    return JSONResponse(content={"item": exchange_rate})

@exchange_rate_router.post("/item")
def create_item(
    data: CreateExchangeRateSchema = Body(),
    db: Session = Depends(get_db),
    _ = Depends(auth_admin),
):
    exchange_rate_service.create_item(db, data)
    return JSONResponse(content={"status": "success"}, status_code=201)

@exchange_rate_router.put("/item/{id}")
def update_item(
    id: str = Path(description="Exchange rate ID"),
    data: UpdateExchangeRateSchema = Body(),
    db: Session = Depends(get_db),
    _ = Depends(auth_admin),
):
    exchange_rate_service.update_item(db, id, data)
    return JSONResponse(content={"status": "success"})

@exchange_rate_router.delete("/item/{id}")
def delete_item(
    id: str = Path(description="Exchange rate ID"),
    db: Session = Depends(get_db),
    _ = Depends(auth_admin),
):
    exchange_rate_service.delete_item(db, id)
    return JSONResponse(content={"status": "success"}, status_code=204)
