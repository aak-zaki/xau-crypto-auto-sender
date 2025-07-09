import time
import requests

RENDER_ENDPOINT = "http://127.0.0.1:5050/notify"
SYMBOLS = {
    "BTCUSDT": {"breakout": 110000, "tp1": 112200, "tp2": 115500, "sl": 108680},
    "ETHUSDT": {"breakout": 2800, "tp1": 2856, "tp2": 2940, "sl": 2766},
    "BNBUSDT": {"breakout": 670, "tp1": 683.4, "tp2": 703.5, "sl": 661.96},
    "SOLUSDT": {"breakout": 160, "tp1": 163.2, "tp2": 168, "sl": 158.08},
    "XAUUSD": {"breakout": 3328, "tp1": 3394, "tp2": 3494, "sl": 3288}
}

def get_price(symbol):
    try:
        if symbol == "XAUUSD":
            url = "https://www.goldapi.io/api/XAU/USD"
            headers = {
                "x-access-token": "goldapi-abp8wesmcva5rpy-io",  # Ganti dengan API KEY asli kamu
                "Content-Type": "application/json"
            }
            r = requests.get(url, headers=headers, timeout=10)
            data = r.json()
            if "ask" in data:
                return float(data["ask"])
            elif "price" in data:
                return float(data["price"])
            else:
                print(f"[XAUUSD] ⚠️ Tidak ada harga dalam respon: {data}")
                return None
        else:
            url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
            r = requests.get(url, timeout=5)
            return float(r.json()["price"])
    except Exception as e:
        print(f"Error getting price for {symbol}:", e)
        return None

def send_alert(message):
    try:
        payload = {"message": message}
        r = requests.post(RENDER_ENDPOINT, json=payload, timeout=5)
        print(f"🔔 Alert sent: {message} | status: {r.status_code}")
    except Exception as e:
        print("Error sending:", e)

prev_status = {}

while True:
    try:
        for symbol, levels in SYMBOLS.items():
            price = get_price(symbol)
            if price:
                status = prev_status.get(symbol, "normal")
                print(f"[{symbol}] Harga: {price:.2f} | Status Sebelumnya: {status}")

                if status == "normal" and price > levels["breakout"]:
                    send_alert(f"🚨 BREAKOUT: {symbol} > {levels['breakout']} (sekarang: {price:.2f})")
                    prev_status[symbol] = "breakout"

                elif status == "breakout":
                    if price >= levels["tp2"]:
                        send_alert(f"✅ TP2 Tercapai: {symbol} di {price:.2f}")
                        prev_status[symbol] = "tp2"
                    elif price >= levels["tp1"]:
                        send_alert(f"✅ TP1 Tercapai: {symbol} di {price:.2f}")
                    elif price <= levels["sl"]:
                        send_alert(f"❌ SL Tersentuh: {symbol} di {price:.2f}")
                        prev_status[symbol] = "normal"
            else:
                print(f"[{symbol}] ❌ Gagal mendapatkan harga.")
    except Exception as e:
        print("⚠️ Loop error:", e)
    time.sleep(60)

