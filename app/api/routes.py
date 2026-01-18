from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.services.price_service import PriceService
from app.schemas import PriceResponse

router = APIRouter(prefix="/api/v1", tags=["prices"])


@router.get("/prices/all", response_model=List[PriceResponse])
def get_all_prices(
        ticker: str = Query(..., description="Ticker symbol (e.g., BTC_USD)"),
        db: Session = Depends(get_db)
):
    service = PriceService(db)
    prices = service.get_all_by_ticker(ticker)

    if not prices:
        raise HTTPException(status_code=404, detail="No data found for this ticker")

    return prices


@router.get("/prices/latest", response_model=PriceResponse)
def get_latest_price(
        ticker: str = Query(..., description="Ticker symbol (e.g., BTC_USD)"),
        db: Session = Depends(get_db)
):
    service = PriceService(db)
    price = service.get_latest_price(ticker)

    if not price:
        raise HTTPException(status_code=404, detail="No data found for this ticker")

    return price


@router.get("/prices/filter", response_model=List[PriceResponse])
def get_prices_by_date(
        ticker: str = Query(..., description="Ticker symbol (e.g., BTC_USD)"),
        date_from: Optional[int] = Query(None, description="Start date (Unix timestamp)"),
        date_to: Optional[int] = Query(None, description="End date (Unix timestamp)"),
        db: Session = Depends(get_db)
):
    service = PriceService(db)
    prices = service.get_prices_by_date(ticker, date_from, date_to)

    if not prices:
        raise HTTPException(status_code=404, detail="No data found for this ticker in specified date range")

    return prices