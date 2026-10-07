from fastapi import APIRouter, Depends, HTTPException

from src.api.dependencies.auth import get_current_user
from src.api.dependencies.clients import get_product_client
from src.api.dependencies.services import get_order_service
from src.clients.product_client import ProductClient
from src.core.response import success_response
from src.schemas.order import CreateOrderRequest, OrderItemResponse, OrderResponse
from src.schemas.response import ApiResponse
from src.services.order_service import OrderService

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    dependencies=[Depends(get_current_user)],
)

async def to_create_order_response(
    order,
    product_client: ProductClient,
) -> OrderResponse:

    items = []

    for item in order.items:
        product = await product_client.get_product(
            item.product_id
        )

        items.append(
            OrderItemResponse(
                product_id=item.product_id,
                product_name=product["name"],
                quantity=item.quantity,
                unit_price=item.unit_price,
            )
        )

    return OrderResponse(
        id=order.id,
        user_id=order.user_id,
        total=order.total,
        status=order.status,
        payment_method=order.payment_method,
        items=items,
    )


async def to_order_response(
    order,
    product_client: ProductClient,
) -> OrderResponse:

    items = []

    for item in order.items:

        product = await product_client.get_product(
            item.product_id
        )

        items.append(
            OrderItemResponse(
                product_id=item.product_id,
                product_name=product["name"],
                quantity=item.quantity,
                unit_price=item.unit_price,
            )
        )

    return OrderResponse(
        id=order.id,
        user_id=order.user_id,
        total=order.total,
        status=order.status,
        payment_method=order.payment_method,
        items=items,
    )


@router.post("", response_model=ApiResponse[OrderResponse], status_code=201)
async def create_order(
    request: CreateOrderRequest,
    current_user: dict = Depends(get_current_user),
    service: OrderService = Depends(get_order_service),
    product_client: ProductClient = Depends(get_product_client),
):
    try:
        user_id = current_user.get("id")
        order = await service.create_order(user_id, request)
        return ApiResponse(
            success=True,
            message="Order created successfully",
            data= await to_order_response(order, product_client),
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


@router.get(
    "",
    response_model=ApiResponse[list[OrderResponse]],
)
async def get_orders(
    current_user: dict = Depends(get_current_user),
    service: OrderService = Depends(get_order_service),
    product_client: ProductClient = Depends(get_product_client),
):
    user_id = current_user["id"]

    orders = service.list_orders(user_id)

    order_responses = []

    for order in orders:
        order_response = await to_order_response(
            order,
            product_client,
        )

        order_responses.append(order_response)

    return success_response(
        message="Orders retrieved successfully",
        data=order_responses,
    )


@router.get("/{order_id}", response_model=ApiResponse[OrderResponse])
async def get_order(
    order_id: str,
    current_user: dict = Depends(get_current_user),
    service: OrderService = Depends(get_order_service),
    product_client: ProductClient = Depends(get_product_client),
):
    try:
        user_id = current_user["id"]
        order = service.get_order_by_id(
            order_id=order_id,
            user_id=user_id,
        )
        return ApiResponse(
            success=True,
            message="Orders retrieved successfully",
            data= await to_order_response(order,product_client),
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error