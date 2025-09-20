import requests
import datetime
import httpx  # async HTTP client

from bs4 import BeautifulSoup

async def get_current_usd_to_ugx():
    url = "https://wise.com/gb/currency-converter/usd-to-ugx-rate"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

        if response.status_code != 200:
            raise Exception("Failed to fetch page")

        soup = BeautifulSoup(response.text, "html.parser")

        # Look for the conversion result (changes over time)
        rate_element = soup.find("div", class_="_midMarketRateAmount_14arr_139")  # https://wise.com/gb/currency-converter/usd-to-ugx-rate  rate container

        if not rate_element:
            raise Exception("Could not find rate element. Page structure may have changed.")

        rate = float(rate_element.text.replace(",", "").split(" ")[3])
        return rate


async def get_coin_price(symbol):
    async with httpx.AsyncClient() as client:

        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        response = await client.get(url)
        data = response.json()
        return float(data["price"])

def readable_time(time_stamp):
    """
    Convert a timestamp in milliseconds (string or int) to human-readable datetime.
    """
    ts = int(time_stamp)  # ensure it's an int
    return datetime.datetime.fromtimestamp(ts / 1000).strftime("%Y-%m-%d %H:%M:%S")

async def get_coin_trend(symbol, limit):
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": "1m",
        "limit": limit  # number of candle sticks
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()

        candlesticks_data = {}

        for index, candlestick in enumerate(data):
            candlestick_data = {
                "open_time": readable_time(candlestick[0]),
                "open_price": candlestick[1],
                "close_time": readable_time(candlestick[6]),
                "close_price": candlestick[4]
            }
            candlesticks_data[index] = candlestick_data

        return candlesticks_data
# currency_data = [1758364980000, '115779.99000000', '115780.00000000', '115779.99000000', '115780.00000000', '1.14482000', 1758365039999, '132547.25326390', 184, '0.51121000', '59187.89380000', '0']
#               Open time(ms) ,    Open price,      High price,         Low price,         Close price       BTC traded,    Close time(ms),   USDT traded,    No.trades BTC bought,  USDT spent  Ignore: 0 (not used)
# Each array inside is one candlestick (1 minute, 5 minutes, etc., depending on the interval you requested).
