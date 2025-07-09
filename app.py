import os
import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = "7667409931:AAGW5AQiBeaT2wsMj6FEGNR5oXFxwBVtww8"
CHAT_ID = "101774290"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("Gagal kirim:", e)

@app.route("/")
def index():
    return "Bot Aktif (Flask)", 200

@app.route("/notify", methods=["POST"])
def notify():
    data = request.json
    message = data.get("message", "Tidak ada pesan.")
    send_telegram(f"📡 Update dari bot:\n{message}")
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
