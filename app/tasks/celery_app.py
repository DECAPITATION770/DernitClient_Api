import asyncio
import time
from celery import Celery
from app.config import settings
from app.database import SessionLocal
from app.services.deribit_client import DeribitClient
from app.services.price_service import PriceService

from app.domain.ticker import Ticker
from app.repositories.price_repository import PriceRepository
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
    asyncio.run(fetch_prices_async())


async def fetch_prices_async():
    tickers = ["BTC", "ETH"]
    timestamp = int(time.time())

    async with DeribitClient() as client:
        db = SessionLocal()
        try:
            repository = PriceRepository(db)
            service = PriceService(repository)

            for ticker in [Ticker.BTC_USD, Ticker.ETH_USD]:
                price = await client.get_index_price(ticker.value.split("_")[0])
                if price:
                    service.save_price(
                        ticker=ticker,
                        price=price,
                        timestamp=timestamp,
                    )
        finally:
            db.close()
