import requests
import pytest

COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"
COINGECKO_PARAMS = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 10,
    "page": 1,
    "sparkline": "false",
}

REQUIRED_FIELDS = [
    "id",
    "symbol",
    "name",
    "current_price",
    "price_change_percentage_24h",
    "market_cap",
]


@pytest.fixture(scope="module")
def coins():
    response = requests.get(COINGECKO_URL, params=COINGECKO_PARAMS)
    assert response.status_code == 200, "CoinGecko API did not return 200"
    return response.json()


def test_coingecko_returns_ten_coins(coins):
    assert len(coins) == 10


def test_each_coin_has_required_fields(coins):
    for coin in coins:
        for field in REQUIRED_FIELDS:
            assert field in coin, f"Missing field '{field}' in coin '{coin.get('id', 'unknown')}'"


def test_coin_prices_are_positive_numbers(coins):
    for coin in coins:
        price = coin["current_price"]
        assert isinstance(price, (int, float)), f"{coin['name']} price is not a number: {price}"
        assert price > 0, f"{coin['name']} has non-positive price: {price}"


def test_coin_price_change_is_numeric(coins):
    for coin in coins:
        change = coin["price_change_percentage_24h"]
        assert change is not None, f"{coin['name']} is missing price_change_percentage_24h"
        assert isinstance(change, (int, float)), f"{coin['name']} price change is not numeric: {change}"


def test_coin_market_cap_is_positive(coins):
    for coin in coins:
        assert coin["market_cap"] > 0, f"{coin['name']} has invalid market cap: {coin['market_cap']}"


def test_expected_coins_are_present(coins, expected_crypto_coins):
    coin_names = [coin["name"] for coin in coins]
    for expected in expected_crypto_coins:
        assert expected in coin_names, f"Expected coin '{expected}' not found in top 10 response"


def test_coins_ordered_by_market_cap_descending(coins):
    market_caps = [coin["market_cap"] for coin in coins]
    assert market_caps == sorted(market_caps, reverse=True), "Coins are not sorted by market cap descending"
