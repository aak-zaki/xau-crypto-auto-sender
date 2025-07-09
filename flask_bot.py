from flask import Flask, request
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = "7667409931:AAGW5AQiBeaT2wsMj6FEGNR5oXFxwBVtww8"
CHAT_ID = "101774290"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(url, json=payload)
        print(f"Telegram Response: {response.status_code} - {response.text}")
    except Exception as e:
        print("Telegram Error:", e)

@app.route("/")
def index():
    return "Bot Aktif (VPS)", 200

@app.route("/notify", methods=["POST"])
def notify():
    data = request.json
    send_telegram(f"""📡 Update dari bot VPS:\n{data.get('message', 'Tidak ada pesan.')}""")
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
