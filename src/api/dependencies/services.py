from fastapi import Depends
from sqlalchemy.orm import Session

from src.api.dependencies.clients import get_product_client
from src.api.dependencies.database import get_db
from src.services.order_service import OrderService


def get_order_service(
    db: Session = Depends(get_db),
) -> OrderService:
    return OrderService(
        session=db,
        product_client=get_product_client(),
    )
