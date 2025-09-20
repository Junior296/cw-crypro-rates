import datetime
import httpx
from bs4 import BeautifulSoup


# ------------------- CURRENCY RATE SCRAPER -------------------

async def get_current_usd_to_ugx():
    url = "https://wise.com/gb/currency-converter/usd-to-ugx-rate"
    headers = {"User-Agent": "Mozilla/5.0"}

    async with httpx.AsyncClient() as client:
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

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    data = response.json()
    return data[symbol]["usd"]


# ------------------- TIMESTAMP UTILITY -------------------

def readable_time_from_seconds(ts):
    return datetime.datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
# ------------------- COINGECKO CANDLES -------------------

async def get_coinbase_candles(product="BTC-USD", granularity=300):
    """
    Fetch recent candlestick data from Coinbase.
    product: e.g., "BTC-USD", "ETH-USD"
    granularity: interval in seconds (e.g., 300 = 5 minutes)
    """
    url = f"https://api.exchange.coinbase.com/products/{product}/candles?granularity={granularity}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()

    # Coinbase returns [time, low, high, open, close, volume]
    candles = [
        {
            "open_time": readable_time_from_seconds(c[0]),
            "open": c[3],
            "high": c[2],
            "low": c[1],
            "close": c[4],
            "volume": c[5]
        }
        for c in data
    ]
    return candles
