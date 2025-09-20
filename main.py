import datetime
import httpx
from bs4 import BeautifulSoup


# ------------------- CURRENCY RATE SCRAPER -------------------

async def get_current_usd_to_ugx():
    url = "https://wise.com/gb/currency-converter/usd-to-ugx-rate"
    headers = {"User-Agent": "Mozilla/5.0"}

    async with httpx.AsyncClient(proxy="http://192.168.43.1:8080") as client:
        response = await client.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception("Failed to fetch page")

    soup = BeautifulSoup(response.text, "html.parser")
    rate_element = soup.find("div", class_="_midMarketRateAmount_14arr_139")

    if not rate_element:
        raise Exception("Could not find rate element. Page structure may have changed.")

    rate = float(rate_element.text.replace(",", "").split(" ")[3])
    return rate


# ------------------- COINGECKO PRICE -------------------

async def get_coin_price_coingecko(symbol="bitcoin"):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"

    async with httpx.AsyncClient(proxy="http://192.168.43.1:8080") as client:
        response = await client.get(url)

    data = response.json()
    return data[symbol]["usd"]


# ------------------- TIMESTAMP UTILITY -------------------

def readable_time(time_stamp):
    """Convert timestamp (ms) to human-readable datetime."""
    ts = int(time_stamp)
    return datetime.datetime.fromtimestamp(ts / 1000).strftime("%Y-%m-%d %H:%M:%S")


# ------------------- COINGECKO CANDLES -------------------

async def get_coingecko_candles(symbol="bitcoin", vs_currency="usd", days=1):
    """
    Get OHLC candlestick data from CoinGecko.
    symbol: "bitcoin", "ethereum", etc.
    vs_currency: "usd", "ugx", etc.
    days: 1, 7, 30, "max"
    """
    url = f"https://api.coingecko.com/api/v3/coins/{symbol}/ohlc"
    params = {"vs_currency": vs_currency, "days": days}

    async with httpx.AsyncClient(proxy="http://192.168.43.1:8080") as client:
        response = await client.get(url, params=params)

    data = response.json()

    candles = [
        {
            "open_time": readable_time(c[0]),
            "open": c[1],
            "high": c[2],
            "low": c[3],
            "close": c[4]
        }
        for c in data
    ]
    return candles
