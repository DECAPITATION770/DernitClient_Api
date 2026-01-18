from typing import List, Optional

from app.domain.ticker import Ticker
from app.models import CryptoPrice
from app.repositories.price_repository import PriceRepository


class PriceService:
    def __init__(self, repository: PriceRepository):
        self.repository = repository

    def save_price(
        self,
        ticker: Ticker,
        price: float,
        timestamp: int,
    ) -> CryptoPrice:
        return self.repository.save(
            ticker=ticker.value,
            price=price,
            timestamp=timestamp,
        )

    def get_all_by_ticker(self, ticker: Ticker, limit: int = 100) -> List[CryptoPrice]:
        return self.repository.get_all_by_ticker(ticker.value, limit)

    def get_latest_price(self, ticker: Ticker) -> Optional[CryptoPrice]:
        return self.repository.get_latest_by_ticker(ticker.value)

    def get_prices_by_date(
        self,
        ticker: Ticker,
        date_from: int,
        date_to: int,
    ) -> List[CryptoPrice]:
        if date_from > date_to:
            raise ValueError("date_from must be <= date_to")

        return self.repository.get_by_date_range(
            ticker=ticker.value,
            date_from=date_from,
            date_to=date_to,
        )
