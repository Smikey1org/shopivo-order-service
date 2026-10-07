import httpx


class ProductClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    async def get_product(self, product_id: str) -> dict:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(
                    f"{self.base_url}/products/{product_id}"
                )

        except httpx.ConnectError as err:
            raise RuntimeError(
                "Product service is unavailable"
            ) from err

        except httpx.TimeoutException as err:
            raise RuntimeError(
                "Product service request timed out"
            ) from err

        except httpx.RequestError as err:
            raise RuntimeError(
                "Unable to communicate with product service"
            ) from err

        if response.status_code == 404:
            raise ValueError(
                "Product not found"
            )

        if response.status_code != 200:
            raise RuntimeError(
                "Product service returned an unexpected response"
            )
        productResponse = response.json()
        return productResponse.get("data")
