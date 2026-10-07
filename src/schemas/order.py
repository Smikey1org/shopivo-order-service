from decimal import Decimal

from pydantic import BaseModel, Field


class CreateOrderItem(BaseModel):
    product_id: str
    quantity: int = Field(gt=0)


class CreateOrderRequest(BaseModel):
    items: list[CreateOrderItem] = Field(min_length=1)
    payment_method: str = "COD"


class OrderItemResponse(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    unit_price: Decimal


class OrderResponse(BaseModel):
    id: str
    user_id: str
    total: Decimal
    status: str
    payment_method: str
    items: list[OrderItemResponse]
