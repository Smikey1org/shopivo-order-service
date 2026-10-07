import httpx


class AuthClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    async def get_user_profile(self, access_token: str) -> dict:
        try:
            client = httpx.AsyncClient()
            response = await client.get(
                f"{self.base_url}/user/profile",
                headers={
                    "Authorization": f"Bearer {access_token}",
                },
            )
        except httpx.ConnectError as err:
            raise RuntimeError(
                "Auth service is unavailable"
            ) from err

        except httpx.TimeoutException as err:
            raise RuntimeError(
                "Auth service request timed out"
            ) from err

        except httpx.RequestError as err:
            raise RuntimeError(
                "Unable to communicate with auth service"
            ) from err

        if response.status_code == 401:
            raise PermissionError(
                "Invalid or expired access token"
            )

        if response.status_code != 200:
            raise RuntimeError(
                "Auth service returned an unexpected response"
            )

        return response.json()