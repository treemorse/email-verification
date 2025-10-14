import os
from flask import Flask
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

@app.route('/send-email')
def send_email():
    SMTP_SERVER = "smtp.timeweb.ru"
    SMTP_PORT = 465
    EMAIL_FROM = "admin@blossomm.ru"
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    EMAIL_TO = os.getenv('EMAIL_TO')

    subject = "Тестовое письмо"
    body = "Это тестовое письмо отправленное через Python скрипт."

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO

    try:
        print("Подключаемся к серверу...")
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        
        print("Логинимся...")
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        
        print("Отправляем письмо...")
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        
        print("✅ Письмо успешно отправлено!")
        server.quit()
        return "✅ Письмо успешно отправлено!"

    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return f"❌ Ошибка: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)