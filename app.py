from flask import Flask, request, jsonify
from main import get_current_usd_to_ugx, get_coin_price, get_coin_trend

app = Flask(__name__)



@app.route("/ugx-rate/")
async def get_ugx_rate():
    rate = await get_current_usd_to_ugx()
    return jsonify({"rate": rate})



@app.route("/get/coin/data/", methods=["POST"])
async def get_coin_data():
    symbol = request.json.get("symbol")
    limit = request.json.get("limit", 5)
    coin_data = await get_coin_trend(symbol, limit)
    return coin_data


@app.route("/get/coin/price/usd/")
async def get_coin_price_usd():
    symbol = request.json.get("symbol")
    coin_price = await get_coin_price(symbol)
    rate = await get_current_usd_to_ugx()
    return jsonify({f"{symbol}": coin_price, "ugx": coin_price * rate})


if __name__ == "__main__":
    app.debug = False
    app.run()
