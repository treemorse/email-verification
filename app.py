import os
from flask import Flask
import smtplib
from email.mime.text import MIMEText
import logging
import threading
import time

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_startup_email():
    SMTP_SERVER = "smtp.timeweb.ru"
    SMTP_PORT = 465
    EMAIL_FROM = "admin@blossomm.ru"
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    EMAIL_TO = os.getenv('EMAIL_TO')

    subject = "🚀 Application Deployed Successfully"
    body = f"""
    Hello!
    
    Your Flask application has been successfully deployed on Timeweb.
    
    Application details:
    - SMTP Server: {SMTP_SERVER}
    - From: {EMAIL_FROM}
    - To: {EMAIL_TO}
    
    This is an automated deployment notification.
    """

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO

    try:
        logger.info("Sending deployment notification email...")
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        server.quit()
        logger.info("✅ Deployment email sent successfully!")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to send deployment email: {e}")
        return False

def delayed_email():
    time.sleep(10)
    send_startup_email()

if os.environ.get('SEND_STARTUP_EMAIL', 'true').lower() == 'true':
    email_thread = threading.Thread(target=delayed_email)
    email_thread.daemon = True
    email_thread.start()

@app.route('/')
def home():
    return "Flask Email App is running! Deployment email has been sent or is being sent."

@app.route('/send-email')
def send_email_endpoint():
    success = send_startup_email()
    if success:
        return "✅ Email sent successfully!"
    else:
        return "❌ Failed to send email", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)