from utils import check_strategy, send_email

assets = ["BTC-USD", "ADVANC.BK"]
email_body = "<html><body><h2>Market Signal Report</h2>"

for ticker in assets:
    res = check_strategy(ticker)
    
    # สร้างเงื่อนไข
    is_buy = (res['rsi'] < 30) or (res['is_buy_zone'] and res['zone_days'] <= 15)
    color = "red" if is_buy else "black"
    signal_text = "BUY SIGNAL" if is_buy else "Wait / Hold"
    
    # ออกแบบ Layout
    email_body += f"""
    <div style="border: 1px solid #ccc; padding: 10px; margin-bottom: 10px; border-radius: 8px;">
        <h3 style="margin: 0;">{res['ticker']}</h3>
        <p style="margin: 5px 0;">Price: <b>{res['price']:.2f}</b> | RSI: <b>{res['rsi']:.2f}</b></p>
        <p style="margin: 5px 0; color: {color};">Status: <b>{signal_text}</b></p>
    </div>
    """

email_body += "</body></html>"
send_email("Daily Investment Update", email_body)
