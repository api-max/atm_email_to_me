import yfinance as yf
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils import check_strategy

# --- Config ---
EMAIL_USER     = os.environ["EMAIL_USER"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
EMAIL_RECEIVER = os.environ["EMAIL_RECEIVER"]

# Portfolio - เรียง A-Z ตามตลาด
TICKERS = [
    # Crypto
    "BTC-USD",
    "BTC-THB",
    "ETH-USD",
    
    # Commodity
    "XAUUSD=X",
    
    # NASDAQ
    "AAPL",
    "GOOGL",
    "MSFT",
    "NVDA",
    
    # SET
    "ADVANC.BK",
    "AOT.BK",
    "CPALL.BK",
    "KBANK.BK",
    "PTT.BK",
    "SCB.BK",
    "^SET.BK",
    "TDEX.BK",
]

# --- Build email body ---
email_body = """
<html>

    

<body style="font-family: Arial, sans-serif; background-color: #f5f5f5;">
<h1 style="text-align: center; color: #333; font-weight: 700;">📊 Daily Portfolio Strategy Report</h1>
<p style="text-align: center; color: #666; font-size: 12px; font-weight: 400;">Generated automatically by Investment Bot</p>
"""

for ticker in TICKERS:
    res = check_strategy(ticker)

    # Guard: ข้ามถ้าดึงข้อมูลไม่ได้หรือ data ไม่พอคำนวณ
    if res is None:
        print(f"[WARN] Skipping {ticker}: insufficient data")
        continue

    # กำหนดสี
    zone_color = "green" if res['is_buy_zone'] else "red"
    zone_text  = "BUY ZONE" if res['is_buy_zone'] else "SELL ZONE"
    
    # เลือกสีสำหรับ event
    event_color = "#28a745" if "Up" in res['cdc_event'] else "#dc3545" if "Down" in res['cdc_event'] else "#6c757d"

    email_body += f"""
    <div style="border: 1px solid #ddd; padding: 15px; margin-bottom: 12px; border-radius: 8px; background-color: #fff; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <h3 style="margin-top: 0; color: #333; font-weight: 700; ">{res['ticker']}</h3>
        <div style="font-size: 16px; line-height: 1.8; ">
            <strong>Price:</strong> {res['price']:.2f} | 
            <strong>RSI:</strong> <span style="color: {'#dc3545' if res['rsi'] > 70 else '#28a745' if res['rsi'] < 30 else '#0066cc'};">{res['rsi']:.2f}</span>
        </div>
        <hr style="border: none; border-top: 1px solid #eee; margin: 10px 0;">
        <div style="margin-top: 10px; line-height: 1.8; ">
            <strong>Status:</strong> <span style="color: {zone_color}; font-weight: 700; padding: 5px 10px; border-radius: 4px; background-color: {'#e8f5e9' if zone_color == 'green' else '#ffebee'};">{zone_text}</span><br>
            <strong>Event:</strong> <span style="color: {event_color}; font-weight: 700;">{res['cdc_event']}</span><br>
            <strong>Duration:</strong> {res['zone_days']} days in {zone_text}
        </div>
    </div>
    """

email_body += """
    <hr style="border: none; border-top: 2px solid #0066cc; margin-top: 40px;">
    <p style="text-align: center; color: #999; font-size: 11px; ">
        This is an automated report. Do not reply to this email.
    </p>
</body></html>
"""

# --- Send email ---
try:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Daily Portfolio Strategy Alert"
    msg["From"]    = EMAIL_USER
    msg["To"]      = EMAIL_RECEIVER
    msg.attach(MIMEText(email_body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USER, EMAIL_RECEIVER, msg.as_string())

    print("[INFO] Email sent successfully.")
except Exception as e:
    print(f"[ERROR] Failed to send email: {e}")
    exit(1)
