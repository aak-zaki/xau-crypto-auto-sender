import requests
import time

RENDER_ENDPOINT = "http://152.42.231.194:5000/notify"
SYMBOLS = ["ETHUSDT", "BTCUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT", "CELOUSDT"]
SLEEP_TIME = 3600  # 1 jam

def get_price(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        r = requests.get(url, timeout=5)
        return float(r.json()["price"])
    except Exception as e:
        print(f"Error getting price for {symbol}:", e)
        return None

def send_to_bot(message):
    payload = {"message": message}
    try:
        r = requests.post(RENDER_ENDPOINT, json=payload, timeout=5)
        print(f"Sent: {message}, status: {r.status_code}")
    except Exception as e:
        print("Error sending:", e)

while True:
    try:
        msg = "📈 Auto Update Harga:\n"
        for sym in SYMBOLS:
            price = get_price(sym)
            if price:
                msg += f"{sym}: {price:.2f}\n"
        # Kirim hanya bagian ini:
        send_to_bot(msg)
    except Exception as e:
        print("Loop error:", e)
    time.sleep(SLEEP_TIME)
