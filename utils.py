import smtplib
import os
import yfinance as yf
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def check_strategy(ticker):
    """ดึงข้อมูลราคาและ RSI (ตัวอย่างเบื้องต้น)"""
    stock = yf.Ticker(ticker)
    data = stock.history(period="1mo")
    
    # คำนวณ RSI ง่ายๆ (หรือใช้ library ta-lib ก็ได้)
    # สมมติ logic ว่าราคาปัจจุบันอยู่ใต้เส้น MA หรือ RSI ต่ำ
    current_price = data['Close'].iloc[-1]
    rsi = 30.0  # แทนค่าการคำนวณจริง
    
    return {
        "ticker": ticker,
        "price": current_price,
        "rsi": rsi,
        "is_prebuy": True if rsi < 40 else False,
        "is_oversold": True if rsi < 30 else False
    }

def send_email(subject, body):
    """ส่งอีเมลผ่าน Gmail"""
    sender_email = os.environ.get("EMAIL_USER")
    password = os.environ.get("EMAIL_PASSWORD") # มาจาก GitHub Secrets
    receiver_email = os.environ.get("EMAIL_RECEIVER")
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, password)
        server.send_message(msg)