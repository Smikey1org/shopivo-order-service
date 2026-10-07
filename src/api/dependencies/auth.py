from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from src.api.dependencies.clients import get_auth_client
from src.clients.auth_client import AuthClient

bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    auth_client: AuthClient = Depends(get_auth_client),
) -> dict:
    access_token = credentials.credentials

    try:
        return await auth_client.get_user_profile(access_token)
    
    except RuntimeError as re:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(re),
            headers={
                "WWW-Authenticate": "Bearer"
            },
        ) from re
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={
                "WWW-Authenticate": "Bearer"
            },
        ) from exc
