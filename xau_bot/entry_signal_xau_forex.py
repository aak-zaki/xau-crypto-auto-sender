import requests
import time

RSI_PERIOD = 14
RSI_LOW = 30
RSI_HIGH = 70
SLEEP_TIME = 3600  # 1 jam
RENDER_ENDPOINT = "http://127.0.0.1:5050/notify"

def get_price():
    try:
        url = "https://api.exchangerate.host/latest?base=XAU&symbols=USD"
        r = requests.get(url, timeout=5)
        data = r.json()
        return float(data["rates"]["USD"])
    except Exception as e:
        print("Error fetching price:", e)
        return None

def calculate_rsi(data):
    if len(data) < RSI_PERIOD + 1:
        return None
    deltas = [data[i] - data[i - 1] for i in range(1, len(data))]
    gains = [d if d > 0 else 0 for d in deltas]
    losses = [-d if d < 0 else 0 for d in deltas]
    avg_gain = sum(gains[-RSI_PERIOD:]) / RSI_PERIOD
    avg_loss = sum(losses[-RSI_PERIOD:]) / RSI_PERIOD or 1
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def send_to_bot(message):
    try:
        r = requests.post(RENDER_ENDPOINT, json={"message": message}, timeout=5)
        print(f"Sent: {message}, status: {r.status_code}")
    except Exception as e:
        print("Error sending:", e)

prices = []
entry_type = None
entry_price = None

while True:
    try:
        price = get_price()
        if price:
            prices.append(price)

            if price > 3328:
                send_to_bot(f"🚀 XAU/USD tembus resistance 3328! (Harga: {price:.2f})")
            elif price < 3312:
                send_to_bot(f"⚠️ XAU/USD jebol support 3312! (Harga: {price:.2f})")

            if len(prices) > 2:
                diff = abs(price - prices[-2])
                if diff > 1.0:
                    send_to_bot(f"📊 Volatilitas tinggi! Selisih: {diff:.2f} USD")

            if len(prices) > RSI_PERIOD + 1:
                rsi = calculate_rsi(prices[-(RSI_PERIOD + 1):])
                print(f"XAU/USD price: {price:.2f}, RSI: {rsi:.2f}")

                if rsi < RSI_LOW and entry_type is None:
                    entry_type = "buy"
                    entry_price = price
                    tp = price + 3
                    send_to_bot(f"🟢 Entry BUY XAU/USD @ {price:.2f}\n🎯 TP: {tp:.2f} | RSI: {rsi:.1f}")
                elif rsi > RSI_HIGH and entry_type is None:
                    entry_type = "sell"
                    entry_price = price
                    tp = price - 3
                    send_to_bot(f"🔴 Entry SELL XAU/USD @ {price:.2f}\n🎯 TP: {tp:.2f} | RSI: {rsi:.1f}")

            if entry_type == "buy" and price >= entry_price + 3:
                send_to_bot(f"✅ TP HIT! BUY XAU/USD dari {entry_price:.2f} → {price:.2f}")
                entry_type = None
                entry_price = None
            elif entry_type == "sell" and price <= entry_price - 3:
                send_to_bot(f"✅ TP HIT! SELL XAU/USD dari {entry_price:.2f} → {price:.2f}")
                entry_type = None
                entry_price = None

            if len(prices) > 4:
                trend = "⬆️ Naik" if prices[-1] > prices[-4] else "⬇️ Turun"
                send_to_bot(f"📈 Trend XAU/USD 3 jam terakhir: {trend}")

    except Exception as e:
        print("Loop error:", e)

    time.sleep(SLEEP_TIME)
