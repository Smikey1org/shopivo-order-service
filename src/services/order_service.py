from decimal import Decimal

from sqlalchemy.orm import Session

from src.clients.product_client import ProductClient
from src.messaging.publisher import publish_order_created
from src.models.order import Order
from src.models.order_item import OrderItem
from src.repositories.order_repository import OrderRepository
from src.schemas.order import CreateOrderRequest


class OrderService:
    def __init__(
        self,
        session: Session,
        product_client: ProductClient,
    ):
        self.session = session
        self.repository = OrderRepository(session)
        self.product_client = product_client

    async def create_order(
        self,
        user_id: str,
        request: CreateOrderRequest,
    ) -> Order:
        if request.payment_method != "COD":
            raise ValueError("Only COD is supported")

        order = Order(
            user_id=user_id,
            total=Decimal("0.00"),
            status="PLACED",
            payment_method="COD",
        )

        total = Decimal("0.00")
        event_items = []

        for request_item in request.items:
            product = await self.product_client.get_product(
                request_item.product_id
            )

            if product["stock"] < request_item.quantity:
                raise ValueError(
                    f"Not enough stock for {product['name']}"
                )

            unit_price = Decimal(str(product["price"]))

            order.items.append(
                OrderItem(
                    product_id=product["id"],
                    quantity=request_item.quantity,
                    unit_price=unit_price,
                )
            )

            total += unit_price * request_item.quantity

            event_items.append({
                "productId": product["id"],
                "productName": product["name"],
                "quantity": request_item.quantity,
            })

        order.total = total

        saved = self.repository.create(order)

        publish_order_created({
            "orderId": saved.id,
            "userId": user_id,
            "items": event_items,
        })

        return saved

    def list_orders(self, user_id: str) -> list[Order]:
        return self.repository.find_by_user(user_id)

    def get_order_by_id(
        self,
        order_id: str,
        user_id: str,
    ) -> Order:
        order = self.repository.find_by_id_and_user(
            order_id,
            user_id,
        )

        if order is None:
            raise ValueError("Order not found")

        return order
