from utils import check_strategy, send_email

def main():
    assets_to_monitor = ["BTC-USD", "ADVANC.BK"]
    email_subject = "Daily Market Signal Report"
    email_body_content = []

    for asset in assets_to_monitor:
        result = check_strategy(asset)
        
        asset_report = f"--- {result['ticker']} ---\n"
        asset_report += f"Current Price: {result['price']:.2f} | RSI: {result['rsi']:.2f}\n"

        if result['is_prebuy'] and result['is_oversold']:
            asset_report += ">>> Signal Detected! (Prebuy + Oversold)\n"
            email_subject = f"MARKET ALERT: Signal for {result['ticker']}!"
        else:
            asset_report += "No significant movement today.\n"
        
        email_body_content.append(asset_report)

    final_email_body = "\n".join(email_body_content)

    try:
        send_email(email_subject, final_email_body)
        print("Successfully sent daily report.")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    main()