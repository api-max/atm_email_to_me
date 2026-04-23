def check_strategy(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="100d")
    
    # ... (คำนวณ RSI เหมือนเดิม) ...
    
    # คำนวณ EMA สำหรับ CDC
    data['EMA12'] = data['Close'].ewm(span=12, adjust=False).mean()
    data['EMA26'] = data['Close'].ewm(span=26, adjust=False).mean()
    
    # สถานะวันนี้และเมื่อวาน
    data['Is_Buy_Zone'] = data['EMA12'] > data['EMA26']
    today_buy = data['Is_Buy_Zone'].iloc[-1]
    yesterday_buy = data['Is_Buy_Zone'].iloc[-2]
    
    # ตรวจจับเหตุการณ์ (Crossover)
    if today_buy and not yesterday_buy:
        event = "Crossed Up (Buy Signal)"
    elif not today_buy and yesterday_buy:
        event = "Crossed Down (Sell Signal)"
    else:
        event = "Continuing Trend"
        
    # นับจำนวนวัน
    data['Zone_Days'] = data['Is_Buy_Zone'].groupby((data['Is_Buy_Zone'] != data['Is_Buy_Zone'].shift()).cumsum()).cumcount() + 1
    
    return {
        "ticker": ticker,
        "price": data['Close'].iloc[-1],
        "rsi": data['RSI'].iloc[-1],
        "is_buy_zone": today_buy,
        "zone_days": data['Zone_Days'].iloc[-1],
        "cdc_event": event
    }
