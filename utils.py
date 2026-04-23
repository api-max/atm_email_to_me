import pandas as pd
import yfinance as yf
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def check_strategy(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="100d")
    
    # คำนวณ RSI (ใช้ pandas คำนวณค่าจริงเสมอ)
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0))
    loss = (-delta.where(delta < 0, 0))
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    data['RSI'] = 100 - (100 / (1 + rs))
    
    # คำนวณ EMA สำหรับ CDC
    data['EMA12'] = data['Close'].ewm(span=12, adjust=False).mean()
    data['EMA26'] = data['Close'].ewm(span=26, adjust=False).mean()
    data['Is_Buy_Zone'] = data['EMA12'] > data['EMA26']
    data['Zone_Days'] = data['Is_Buy_Zone'].groupby((data['Is_Buy_Zone'] != data['Is_Buy_Zone'].shift()).cumsum()).cumcount() + 1
    
    return {
        "ticker": ticker,
        "price": data['Close'].iloc[-1],
        "rsi": data['RSI'].iloc[-1],
        "is_buy_zone": data['Is_Buy_Zone'].iloc[-1],
        "zone_days": data['Zone_Days'].iloc[-1]
    }

def send_email(subject, html_content):
    sender_email = os.environ.get("EMAIL_USER")
    password = os.environ.get("EMAIL_PASSWORD")
    receiver_email = os.environ.get("EMAIL_RECEIVER")
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    # เปลี่ยนเป็น 'html' แทน 'plain'
    msg.attach(MIMEText(html_content, 'html'))
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, password)
        server.send_message(msg)
