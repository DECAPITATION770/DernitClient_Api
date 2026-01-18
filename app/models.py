from sqlalchemy import Column, Integer, String, Float, BigInteger, Index
from app.database import Base


class CryptoPrice(Base):
    __tablename__ = "crypto_prices"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, nullable=False, index=True)
    price = Column(Float, nullable=False)
    timestamp = Column(BigInteger, nullable=False, index=True)

    __table_args__ = (
        Index('idx_ticker_timestamp', 'ticker', 'timestamp'),
    )