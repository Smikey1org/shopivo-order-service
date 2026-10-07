from fastapi import FastAPI
from fastapi.exceptions import HTTPException

from src.api.dependencies.database import engine
from src.api.routes.orders import router as order_router
from src.core.config import settings
from src.core.exceptions import http_exception_handler
from src.models.base import Base

# Basic learning setup.
# In production use Alembic migrations instead of create_all().
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.add_exception_handler(
    HTTPException,
    http_exception_handler,
)
app.include_router(order_router)

@app.get("/")
def init():
    return {
        "status": "ok",
        "message": "Welcome to Order API",
        "service": "order",
        "database": "Postgres SQL",
        "language": "Python",
        "framework": "FastAPI",
    }

@app.get("/health")
def health():
    return {
        "service": "order-service",
        "status": "ok",
    }
