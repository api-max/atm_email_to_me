import yfinance as yf
import pandas as pd

def check_strategy(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="100d")
    print(f"[DEBUG] {ticker} columns: {data.columns.tolist()}")
    print(f"[DEBUG] {ticker} sample:\n{data[['Close']].tail(3)}")

    if data.empty or len(data) < 27:
        return None

    # --- Flatten multi-level columns (แก้ปัญหาหุ้นไทย NaN) ---
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    # --- ตรวจสอบว่ามีคอลัมน์ Close จริงๆ ---
    if 'Close' not in data.columns or data['Close'].isnull().all():
        return None

    # --- คำนวณ RSI (14-period) ---
    delta = data['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(com=13, adjust=False).mean()
    avg_loss = loss.ewm(com=13, adjust=False).mean()
    rs = avg_gain / avg_loss
    data['RSI'] = 100 - (100 / (1 + rs))

    # --- คำนวณ EMA สำหรับ CDC ---
    data['EMA12'] = data['Close'].ewm(span=12, adjust=False).mean()
    data['EMA26'] = data['Close'].ewm(span=26, adjust=False).mean()

    # --- สถานะวันนี้และเมื่อวาน ---
    data['Is_Buy_Zone'] = data['EMA12'] > data['EMA26']
    today_buy = bool(data['Is_Buy_Zone'].iloc[-1])
    yesterday_buy = bool(data['Is_Buy_Zone'].iloc[-2])

    # --- ตรวจจับเหตุการณ์ (Crossover) ---
    if today_buy and not yesterday_buy:
        event = "Crossed Up (Buy Signal)"
    elif not today_buy and yesterday_buy:
        event = "Crossed Down (Sell Signal)"
    else:
        event = "Continuing Trend"

    # --- นับจำนวนวันใน Zone ปัจจุบัน ---
    group_id = (data['Is_Buy_Zone'] != data['Is_Buy_Zone'].shift()).cumsum()
    data['Zone_Days'] = data.groupby(group_id).cumcount() + 1

    return {
        "ticker": ticker,
        "price": round(data['Close'].iloc[-1], 2),
        "rsi": round(data['RSI'].iloc[-1], 2),
        "is_buy_zone": today_buy,
        "zone_days": int(data['Zone_Days'].iloc[-1]),
        "cdc_event": event
    }
