import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from flask import current_app


def send_email(recipient, subject, html):
    """Send HTML email when SMTP is configured; otherwise log a safe preview."""
    host = current_app.config.get("SMTP_HOST")
    sender = current_app.config.get("SMTP_FROM_EMAIL")
    if not host or not sender:
        current_app.logger.warning("Email not sent because SMTP is not configured: %s", subject)
        return False

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = recipient
    message.attach(MIMEText(html, "html"))
    with smtplib.SMTP(host, current_app.config["SMTP_PORT"], timeout=15) as smtp:
        smtp.starttls()
        username = current_app.config.get("SMTP_USERNAME")
        if username:
            smtp.login(username, current_app.config.get("SMTP_PASSWORD", ""))
        smtp.sendmail(sender, [recipient], message.as_string())
    return True


def send_google_chat_webhook(message):
    webhook_url = current_app.config.get("GOOGLE_CHAT_WEBHOOK_URL")
    if not webhook_url:
        return False
    response = requests.post(webhook_url, json={"text": message}, timeout=15)
    response.raise_for_status()
    return True
