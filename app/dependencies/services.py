from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.price_repository import PriceRepository
from app.services.price_service import PriceService


def get_price_service(
    db: Session = Depends(get_db),
) -> PriceService:
    repository = PriceRepository(db)
    return PriceService(repository)
