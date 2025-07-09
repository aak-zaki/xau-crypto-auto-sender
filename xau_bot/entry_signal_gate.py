import time
import requests
import numpy as np

SYMBOLS = ["BTC_USDT", "BNB_USDT", "SOL_USDT", "ETH_USDT"]
RSI_PERIOD = 14
RSI_LOW = 30
RSI_HIGH = 70
INTERVAL = 60 * 15  # setiap 15 menit
RENDER_ENDPOINT = "http://127.0.0.1:5050/notify"

def calculate_rsi_wilders(closes, period=14):
    if len(closes) < period + 1:
        return None
    deltas = np.diff(closes)
    seed = deltas[:period]
    gain = np.where(seed > 0, seed, 0).sum() / period
    loss = np.where(seed < 0, -seed, 0).sum() / period
    avg_gain = gain
    avg_loss = loss
    for delta in deltas[period:]:
        gain = max(delta, 0)
        loss = max(-delta, 0)
        avg_gain = (avg_gain * (period - 1) + gain) / period
        avg_loss = (avg_loss * (period - 1) + loss) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return round(rsi, 2)

def get_candles(symbol):
    try:
        params = {"currency_pair": symbol, "interval": "5m", "limit": 100}
        r = requests.get("https://api.gateio.ws/api/v4/spot/candlesticks", params=params, timeout=5)
        if r.status_code == 200:
            return [float(c[2]) for c in r.json()]
    except Exception as e:
        print(f"Error get candle {symbol}: {e}")
    return []

def send_to_bot(message):
    try:
        r = requests.post(RENDER_ENDPOINT, json={"message": message}, timeout=5)
        print(f"Sent: {message}, status: {r.status_code}")
    except Exception as e:
        print("Error sending:", e)

while True:
    try:
        for sym in SYMBOLS:
            closes = get_candles(sym)
            if closes:
                rsi = calculate_rsi_wilders(closes, RSI_PERIOD)
                if rsi is not None:
                    if rsi < RSI_LOW:
                        send_to_bot(f"🔽 {sym} RSI {rsi:.1f} ⬅️ OVERSOLD (BUY Signal)")
                    elif rsi > RSI_HIGH:
                        send_to_bot(f"🔼 {sym} RSI {rsi:.1f} ⬅️ OVERBOUGHT (SELL Signal)")
    except Exception as e:
        print("Loop error:", e)
    time.sleep(INTERVAL)

