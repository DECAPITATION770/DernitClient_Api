import asyncio
import time
from celery import Celery
from app.config import settings
from app.database import SessionLocal
from app.services.derbit_client import DeribitClient
from app.services.price_service import PriceService

celery_app = Celery(
    "crypto_tracker",
    broker=settings.redis_url,
    backend=settings.redis_url
)

celery_app.conf.beat_schedule = {
    'fetch-prices-every-minute': {
        'task': 'app.tasks.celery_app.fetch_crypto_prices',
        'schedule': 60.0,
    },
}


@celery_app.task
def fetch_crypto_prices():
    """Периодическая задача для получения цен"""
    asyncio.run(fetch_prices_async())


async def fetch_prices_async():
    tickers = ["BTC", "ETH"]
    timestamp = int(time.time())

    async with DeribitClient() as client:
        db = SessionLocal()
        try:
            service = PriceService(db)

            for ticker in tickers:
                price = await client.get_index_price(ticker)
                if price:
                    service.save_price(
                        ticker=f"{ticker}_USD",
                        price=price,
                        timestamp=timestamp
                    )
                    print(f"Saved {ticker}_USD: {price} at {timestamp}")
        finally:
            db.close()