from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.models.base import Base
from app.routers.auth import auth_router
from app.routers.exchange_rate import exchange_rate_router
from app.routers.wallet import wallet_router
from app.routers.transaction import transaction_router
from app.database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Exchange Rate API", version="0.0.1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
)
app.include_router(auth_router)
app.include_router(exchange_rate_router)
app.include_router(wallet_router)
app.include_router(transaction_router)

app.mount("/", StaticFiles(directory="public/static", html=True), name="static")
