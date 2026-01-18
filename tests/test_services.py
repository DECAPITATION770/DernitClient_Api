import pytest
from unittest.mock import Mock, AsyncMock, patch
from app.services.deribit_client import DeribitClient
from app.services.price_service import PriceService
from app.models import CryptoPrice


@pytest.mark.asyncio
async def test_deribit_client_get_index_price():
    client = DeribitClient()

    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value={
        "result": {"index_price": 45000.5}
    })

    with patch.object(client, 'session') as mock_session:
        mock_session.get.return_value.__aenter__.return_value = mock_response

        price = await client.get_index_price("BTC")
        assert price == 45000.5


def test_price_service_save_price():
    mock_db = Mock()
    service = PriceService(mock_db)

    price = service.save_price("BTC_USD", 45000.5, 1234567890)

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()


def test_price_service_get_latest_price():
    mock_db = Mock()
    service = PriceService(mock_db)

    mock_query = Mock()
    mock_db.query.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    mock_query.first.return_value = CryptoPrice(
        id=1, ticker="BTC_USD", price=45000.5, timestamp=1234567890
    )

    result = service.get_latest_price("BTC_USD")

    assert result.ticker == "BTC_USD"
    assert result.price == 45000.5