from unittest.mock import Mock
from app.services.price_service import PriceService
from app.domain.ticker import Ticker
from app.models import CryptoPrice


def test_save_price():
    mock_repo = Mock()
    mock_repo.save.return_value = CryptoPrice(
        ticker="BTC_USD",
        price=45000.5,
        timestamp=1234567890,
    )

    service = PriceService(mock_repo)

    result = service.save_price(
        ticker=Ticker.BTC_USD,
        price=45000.5,
        timestamp=1234567890,
    )

    mock_repo.save.assert_called_once_with(
        ticker="BTC_USD",
        price=45000.5,
        timestamp=1234567890,
    )
    assert result.ticker == "BTC_USD"


def test_get_latest_price():
    mock_repo = Mock()
    mock_repo.get_latest_by_ticker.return_value = CryptoPrice(
        ticker="ETH_USD",
        price=3200.0,
        timestamp=1234567891,
    )

    service = PriceService(mock_repo)

    result = service.get_latest_price(Ticker.ETH_USD)

    mock_repo.get_latest_by_ticker.assert_called_once_with("ETH_USD")
    assert result.price == 3200.0


def test_get_prices_by_date_invalid_range():
    mock_repo = Mock()
    service = PriceService(mock_repo)

    try:
        service.get_prices_by_date(
            ticker=Ticker.BTC_USD,
            date_from=200,
            date_to=100,
        )
        assert False, "ValueError was not raised"
    except ValueError:
        assert True
