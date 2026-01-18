import aiohttp
from typing import Optional
from app.config import settings


class DeribitClient:
    def __init__(self):
        self.base_url = settings.deribit_api_url
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def get_index_price(self, currency: str) -> Optional[float]:
        if not self.session:
            self.session = aiohttp.ClientSession()

        url = f"{self.base_url}/public/get_index_price"
        params = {"index_name": f"{currency.lower()}_usd"}

        try:
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("result", {}).get("index_price")
                return None
        except Exception as e:
            print(f"Error fetching price for {currency}: {e}")
            return None

    async def close(self):
        if self.session:
            await self.session.close()