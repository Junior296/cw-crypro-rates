from flask import Flask, request, jsonify
from main import get_current_usd_to_ugx, get_coin_price_coingecko, get_coingecko_candles

app = Flask(__name__)


@app.route("/ugx-rate/")
async def get_ugx_rate():
    try:
        rate = await get_current_usd_to_ugx()
        return jsonify({"rate": rate})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/get/coin/data/", methods=["POST"])
async def get_coin_data():
    try:
        symbol = request.json.get("symbol", "bitcoin")
        days = request.json.get("days", 1)  # default: last 1 day
        coin_data = await get_coingecko_candles(symbol, "usd", days)
        return jsonify(coin_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/get/coin/price/usd/", methods=["POST"])
async def get_coin_price_usd():
    try:
        symbol = request.json.get("symbol")
        print(symbol)
        coin_price = await get_coin_price_coingecko(symbol)
        rate = await get_current_usd_to_ugx()
        return jsonify({f"{symbol}": coin_price, "ugx": coin_price * rate})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.debug = False
    app.run()
