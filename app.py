import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

PI_API_KEY = os.environ.get("PI_API_KEY", "").strip()
PI_API_BASE = "https://api.minepi.com/v2"

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "DevAI Study Render Payment Server Running"})

@app.route("/approve", methods=["POST", "OPTIONS"])
def approve_payment():
    if request.method == "OPTIONS":
        return jsonify({}), 200
    data = request.get_json() or {}
    payment_id = data.get("paymentId")
    if not payment_id:
        return jsonify({"error": "paymentId missing"}), 400

    headers = {
        "Authorization": f"Key {PI_API_KEY}",
        "Content-Type": "application/json"
    }
    res = requests.post(f"{PI_API_BASE}/payments/{payment_id}/approve", headers=headers)
    return jsonify(res.json()), res.status_code

@app.route("/complete", methods=["POST", "OPTIONS"])
def complete_payment():
    if request.method == "OPTIONS":
        return jsonify({}), 200
    data = request.get_json() or {}
    payment_id = data.get("paymentId")
    txid = data.get("txid")
    if not payment_id or not txid:
        return jsonify({"error": "paymentId or txid missing"}), 400

    headers = {
        "Authorization": f"Key {PI_API_KEY}",
        "Content-Type": "application/json"
    }
    res = requests.post(
        f"{PI_API_BASE}/payments/{payment_id}/complete",
        json={"txid": txid},
        headers=headers
    )
    return jsonify(res.json()), res.status_code

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

