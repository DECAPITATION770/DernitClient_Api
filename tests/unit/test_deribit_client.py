import pytest
from unittest.mock import Mock, AsyncMock, patch
from app.services.deribit_client import DeribitClient


@pytest.mark.asyncio
async def test_get_index_price_success():
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value={
        "result": {"index_price": 45000.5}
    })

    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_get.return_value.__aenter__.return_value = mock_response

        async with DeribitClient() as client:
            price = await client.get_index_price("BTC")

    assert price == 45000.5


@pytest.mark.asyncio
async def test_get_index_price_error():
    mock_response = Mock()
    mock_response.status = 500

    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_get.return_value.__aenter__.return_value = mock_response

        async with DeribitClient() as client:
            price = await client.get_index_price("BTC")

    assert price is None
