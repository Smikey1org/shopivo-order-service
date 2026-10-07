import httpx


class CartClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    async def get_cart(self, user_id: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/cart/{user_id}"
            )

        if response.status_code != 200:
            raise ValueError("Could not retrieve cart")

        return response.json()
