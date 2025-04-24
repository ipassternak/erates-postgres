from pydantic import BaseModel, Field
from app.models.base import Currency

class GetExchangeRateListSchema(BaseModel):
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

class CreateExchangeRateSchema(BaseModel):
    from_currency: Currency = Field(
        description="From currency"
    )
    to_currency: Currency = Field(
        description="To currency"
    )
    rate: float = Field(
        gt=0,
        minimum=0.0001,
        maximum=1000000000,
        description="Exchange rate"
    )

class UpdateExchangeRateSchema(BaseModel):
    rate: float = Field(
        gt=0,
        minimum=0.0001,
        maximum=1000000000,
        description="Exchange rate"
    )
