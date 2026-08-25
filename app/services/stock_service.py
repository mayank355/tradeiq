import requests

from app.config import settings

ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"


def get_stock_quote(ticker: str) -> dict | None:
    """
    Fetch a live stock quote from Alpha Vantage for the given ticker.
    Returns None if the ticker is invalid or the API call fails/rate-limits,
    rather than raising - a missing live price should degrade gracefully,
    not break the whole query.
    """
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": ticker,
        "apikey": settings.alpha_vantage_api_key,
    }

    try:
        response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException:
        return None

    quote = data.get("Global Quote")
    if not quote or "05. price" not in quote:
        # Alpha Vantage returns an empty {} for invalid tickers, and a
        # "Note" or "Information" key when the rate limit is hit -
        # either way, there's no usable quote data.
        return None

    return {
        "ticker": ticker,
        "price": quote.get("05. price"),
        "change": quote.get("09. change"),
        "change_percent": quote.get("10. change percent"),
        "volume": quote.get("06. volume"),
        "latest_trading_day": quote.get("07. latest trading day"),
    }
