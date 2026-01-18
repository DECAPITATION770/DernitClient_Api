import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from app.main import app
from app.models import CryptoPrice

client = TestClient(app)


@patch('app.api.routes.get_db')
def test_get_latest_price(mock_get_db):
    mock_db = Mock()
    mock_get_db.return_value = mock_db

    with patch('app.api.routes.PriceService') as mock_service:
        mock_instance = mock_service.return_value
        mock_instance.get_latest_price.return_value = CryptoPrice(
            id=1, ticker="BTC_USD", price=45000.5, timestamp=1234567890
        )

        response = client.get("/api/v1/prices/latest?ticker=BTC_USD")

        assert response.status_code == 200
        assert response.json()["ticker"] == "BTC_USD"
        assert response.json()["price"] == 45000.5


@patch('app.api.routes.get_db')
def test_get_latest_price_not_found(mock_get_db):
    mock_db = Mock()
    mock_get_db.return_value = mock_db

    with patch('app.api.routes.PriceService') as mock_service:
        mock_instance = mock_service.return_value
        mock_instance.get_latest_price.return_value = None

        response = client.get("/api/v1/prices/latest?ticker=UNKNOWN")

        assert response.status_code == 404