# ... (ใน loop ของ main.py) ...
    res = check_strategy(ticker)
    
    # กำหนดสี
    zone_color = "green" if res['is_buy_zone'] else "red"
    zone_text = "BUY ZONE" if res['is_buy_zone'] else "SELL ZONE"
    
    email_body += f"""
    <div style="border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 10px; font-family: sans-serif;">
        <h2 style="margin-top: 0;">{res['ticker']}</h2>
        <div style="font-size: 16px;">
            Price: <b>{res['price']:.2f}</b> | RSI: <b>{res['rsi']:.2f}</b>
        </div>
        <hr>
        <div style="margin-top: 10px;">
            Status: <b style="color: {zone_color};">{zone_text}</b><br>
            Event: <b>{res['cdc_event']}</b><br>
            Duration: <b>{res['zone_days']} days</b>
        </div>
    </div>
    """
