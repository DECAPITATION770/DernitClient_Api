from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List

from app.schemas import PriceResponse
from app.domain.ticker import Ticker
from app.services.price_service import PriceService
from app.dependencies.services import get_price_service

router = APIRouter(prefix="/api/v1/prices", tags=["prices"])


@router.get("", response_model=List[PriceResponse])
def get_all_prices(
    ticker: Ticker = Query(...),
    service: PriceService = Depends(get_price_service),
):
    return service.get_all_by_ticker(ticker)


@router.get("/latest", response_model=PriceResponse)
def get_latest_price(
    ticker: Ticker = Query(...),
    service: PriceService = Depends(get_price_service),
):
    price = service.get_latest_price(ticker)

    if not price:
        raise HTTPException(
            status_code=404,
            detail="No data found for this ticker",
        )

    return price


@router.get("/by-date", response_model=List[PriceResponse])
def get_prices_by_date(
    ticker: Ticker = Query(...),
    date_from: int = Query(..., ge=0),
    date_to: int = Query(..., ge=0),
    service: PriceService = Depends(get_price_service),
):
    try:
        return service.get_prices_by_date(
            ticker=ticker,
            date_from=date_from,
            date_to=date_to,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
