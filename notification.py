import os
import smtplib
from email.mime.text import MIMEText
import requests
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

EMAIL_SENDER = os.getenv("EMAIL_SENDER", "nagashreemn09@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "arnpodisxcpgxcpi")  # App password
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER", "nagashreemn07@gmail.com")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def send_notification(subject, message):
    """Send notification via Email and Slack (if configured)."""
    # 1️ Send Email
    try:
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = f"Nagashree <{EMAIL_SENDER}>"
        msg["To"] = EMAIL_RECEIVER

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)

        print(" Email sent successfully!")

    except Exception as e:
        print(" Error sending email:", e)

    # 2 Send Slack
    if SLACK_WEBHOOK_URL:
        try:
            payload = {"text": f"*{subject}*\n{message}"}
            resp = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=10)
            if resp.status_code == 200:
                print(" Slack notification sent successfully!")
            else:
                print(f" Slack notification failed with status {resp.status_code}: {resp.text}")
        except Exception as e:
            print(" Error sending Slack notification:", e)
    else:
        print(" SLACK_WEBHOOK_URL not configured, skipping Slack notification.")


if __name__ == "__main__":
    send_notification("Test Notification", "This is a test message from GDPR scraper.")
