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

TICKERS = [
    "PTT.BK", "ADVANC.BK", "AOT.BK", "CPALL.BK", "KBANK.BK",
    # เพิ่ม ticker ที่ต้องการได้เลย
]

# --- Build email body ---
email_body = """
<html><body>
<h1 style="font-family: sans-serif;">📊 Daily Strategy Report</h1>
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

email_body += "</body></html>"

# --- Send email ---
msg = MIMEMultipart("alternative")
msg["Subject"] = "📈 Daily Strategy Alert"
msg["From"]    = EMAIL_USER
msg["To"]      = EMAIL_RECEIVER
msg.attach(MIMEText(email_body, "html"))

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(EMAIL_USER, EMAIL_PASSWORD)
    server.sendmail(EMAIL_USER, EMAIL_RECEIVER, msg.as_string())

print("[INFO] Email sent successfully.")
