from pydantic import BaseModel, Field
from app.models.base import Currency

class GetTransactionListSchema(BaseModel):
    page: int = Field(
        default=1,
        gt=0,
        description="Page"
    )
    page_size: int = Field(
        default=10,
        gt=0,
        description="Page size"
    )
    from_currency: Currency | None = Field(
        default=None,
        description="From currency"
    )
    to_currency: Currency | None = Field(
        default=None,
        description="To currency"
    )

class CreateTransactionSchema(BaseModel):
    from_wallet_id: str = Field(
        description="From wallet ID"
    )
    to_wallet_id: str = Field(
        description="To wallet ID"
    )
    exchange_rate_id: str = Field(
        description="Exchange rate ID"
    )
    amount: float = Field(
        gt=0,
        minimum=0.0001,
        maximum=1000000000,
        description="Transaction amount"
    )
