from sqlalchemy.orm import Session
from typing import List, Optional
from app.models import CryptoPrice
from app.schemas import PriceFilter


class PriceService:
    def __init__(self, db: Session):
        self.db = db

    def save_price(self, ticker: str, price: float, timestamp: int) -> CryptoPrice:
        db_price = CryptoPrice(
            ticker=ticker,
            price=price,
            timestamp=timestamp
        )
        self.db.add(db_price)
        self.db.commit()
        self.db.refresh(db_price)
        return db_price

    def get_all_by_ticker(self, ticker: str) -> List[CryptoPrice]:
        return self.db.query(CryptoPrice).filter(
            CryptoPrice.ticker == ticker
        ).order_by(CryptoPrice.timestamp.desc()).all()

    def get_latest_price(self, ticker: str) -> Optional[CryptoPrice]:
        return self.db.query(CryptoPrice).filter(
            CryptoPrice.ticker == ticker
        ).order_by(CryptoPrice.timestamp.desc()).first()

    def get_prices_by_date(
            self,
            ticker: str,
            date_from: Optional[int] = None,
            date_to: Optional[int] = None
    ) -> List[CryptoPrice]:
        query = self.db.query(CryptoPrice).filter(
            CryptoPrice.ticker == ticker
        )

        if date_from:
            query = query.filter(CryptoPrice.timestamp >= date_from)

        if date_to:
            query = query.filter(CryptoPrice.timestamp <= date_to)

        return query.order_by(CryptoPrice.timestamp.desc()).all()