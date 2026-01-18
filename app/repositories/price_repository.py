from sqlalchemy.orm import Session
from typing import List, Optional

from app.models import CryptoPrice


class PriceRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(
        self,
        ticker: str,
        price: float,
        timestamp: int,
    ) -> CryptoPrice:
        entity = CryptoPrice(
            ticker=ticker,
            price=price,
            timestamp=timestamp,
        )
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def get_all_by_ticker(self, ticker: str) -> List[CryptoPrice]:
        return (
            self.db.query(CryptoPrice)
            .filter(CryptoPrice.ticker == ticker)
            .order_by(CryptoPrice.timestamp.desc())
            .all()
        )

    def get_latest_by_ticker(self, ticker: str) -> Optional[CryptoPrice]:
        return (
            self.db.query(CryptoPrice)
            .filter(CryptoPrice.ticker == ticker)
            .order_by(CryptoPrice.timestamp.desc())
            .first()
        )

    def get_by_date_range(
        self,
        ticker: str,
        date_from: int,
        date_to: int,
    ) -> List[CryptoPrice]:
        query = self.db.query(CryptoPrice).filter(
            CryptoPrice.ticker == ticker
        )

        if date_from is not None:
            query = query.filter(CryptoPrice.timestamp >= date_from)

        if date_to is not None:
            query = query.filter(CryptoPrice.timestamp <= date_to)

        return query.order_by(CryptoPrice.timestamp.desc()).all()
