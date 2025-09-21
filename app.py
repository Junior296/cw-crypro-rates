from flask import Flask, request, jsonify
from main import get_current_usd_to_ugx, get_coin_price_coingecko, get_coinbase_candles

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
        # Get symbol like "BTC-USD" or default to "BTC-USD"
        symbol = request.json.get("symbol")
        # granularity in seconds, default 5-minute candles
        granularity = request.json.get("granularity")

        coin_data = await get_coinbase_candles(product=symbol, granularity=granularity)
        return jsonify(coin_data[:20])  # return last 5 candles
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
