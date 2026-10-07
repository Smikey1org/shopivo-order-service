from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from src.models.order import Order


class OrderRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, order: Order) -> Order:
        self.session.add(order)
        self.session.commit()
        self.session.refresh(order)
        return order

    def find_by_user(self, user_id: str) -> list[Order]:
        statement = (
            select(Order)
            .where(Order.user_id == user_id)
            .options(joinedload(Order.items))
            .order_by(Order.created_at.desc())
        )

        return (
            self.session.execute(statement)
            .unique()
            .scalars()
            .all()
        )

    def find_by_id_and_user(
        self,
        order_id: str,
        user_id: str,
    ) -> Order | None:
        statement = (
            select(Order)
            .where(
                Order.id == order_id,
                Order.user_id == user_id,
            )
            .options(joinedload(Order.items))
        )

        return (
            self.session.execute(statement)
            .unique()
            .scalars()
            .first()
        )


