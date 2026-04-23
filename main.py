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
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: Arial, sans-serif; background-color: #ffffff; margin: 0; padding: 16px;">
<h1 style="font-size: 22px; color: #333;">📊 Daily Strategy Report</h1>
<p style="color: #666; font-size: 12px;">Generated automatically by Investment Bot</p>
"""

for ticker in TICKERS:
    res = check_strategy(ticker)

    if res is None:
        print(f"[WARN] Skipping {ticker}: insufficient data")
        continue

    zone_color = "green" if res['is_buy_zone'] else "red"
    zone_text  = "BUY ZONE" if res['is_buy_zone'] else "SELL ZONE"
    event_color = "#28a745" if "Up" in res['cdc_event'] else "#dc3545" if "Down" in res['cdc_event'] else "#6c757d"

    email_body += f"""
    <div style="border: 1px solid #ddd; padding: 20px; margin-bottom: 12px; border-radius: 8px; background-color: #fff; font-family: Arial, sans-serif;">
        <h3 style="margin: 0 0 12px 0; font-size: 16px; color: #000;">{res['ticker']}</h3>
        <p style="margin: 0 0 16px 0; font-size: 15px; color: #333;">
            Price: <b>{res['price']:.2f}</b> &nbsp;|&nbsp; RSI: <b>{res['rsi']:.2f}</b>
        </p>
        <hr style="border: none; border-top: 1px solid #eee; margin: 0 0 14px 0;">
        <p style="margin: 0; font-size: 14px; line-height: 2; color: #333;">
            Status: <b style="color: {zone_color};">{zone_text}</b><br>
            Event: <b style="color: {event_color};">{res['cdc_event']}</b><br>
            Duration: <b>{res['zone_days']} days</b>
        </p>
    </div>
    """

email_body += """
    <p style="text-align: center; color: #999; font-size: 11px; margin-top: 24px;">
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
