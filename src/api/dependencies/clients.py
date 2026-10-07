from src.clients.auth_client import AuthClient
from src.clients.product_client import ProductClient
from src.core.config import settings


def get_auth_client() -> AuthClient:
    return AuthClient(base_url=settings.auth_service_url)


def get_product_client() -> AuthClient:
    return ProductClient(base_url=settings.product_service_url)