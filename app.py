from flask import Flask, request, jsonify
from main import get_current_usd_to_ugx, get_coin_price, get_coin_trend

app = Flask(__name__)


@app.route("/ugx-rate/")
def get_ugx_rate():
    try:
        rate = get_current_usd_to_ugx()
        return jsonify({"rate": rate})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/get/coin/data/", methods=["POST"])
def get_coin_data():
    try:
        symbol = request.json.get("symbol")
        limit = request.json.get("limit", 5)
        coin_data = get_coin_trend(symbol, limit)
        return jsonify(coin_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/get/coin/price/usd/", methods=["POST"])
def get_coin_price_usd():
    try:
        symbol = request.json.get("symbol")
        coin_price = get_coin_price(symbol)
        rate = get_current_usd_to_ugx()
        return jsonify({f"{symbol}": coin_price, "ugx": coin_price * rate})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.debug = False
    app.run()
