import smtplib
from src.config import SENDER_MAIL, PASSWORD_MAIL
from src.utils import app


@app.task
def send_email_task(recipient, message):
    sender = SENDER_MAIL
    password = PASSWORD_MAIL
    try:
        with smtplib.SMTP_SSL('smtp.mail.ru', 465) as server:
            server.login(sender, password)
            server.sendmail(sender, recipient, message)
    except Exception as e:
        print(f"Failed to send email: {e}")
