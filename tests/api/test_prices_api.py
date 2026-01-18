from fastapi.testclient import TestClient
from unittest.mock import Mock

from app.main import app
from app.domain.ticker import Ticker
from app.dependencies.services import get_price_service
from app.models import CryptoPrice

client = TestClient(app)


def test_get_latest_price_success():
    mock_service = Mock()
    mock_service.get_latest_price.return_value = CryptoPrice(
        id=1,
        ticker="BTC_USD",
        price=45000.5,
        timestamp=1234567890,
    )

    app.dependency_overrides[get_price_service] = lambda: mock_service

    response = client.get("/api/v1/prices/latest?ticker=BTC_USD")

    assert response.status_code == 200
    assert response.json()["price"] == 45000.5

    app.dependency_overrides.clear()


def test_get_latest_price_not_found():
    mock_service = Mock()
    mock_service.get_latest_price.return_value = None

    app.dependency_overrides[get_price_service] = lambda: mock_service

    response = client.get("/api/v1/prices/latest?ticker=BTC_USD")

    assert response.status_code == 404

    app.dependency_overrides.clear()
