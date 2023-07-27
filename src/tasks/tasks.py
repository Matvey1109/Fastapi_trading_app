import smtplib
from email.message import EmailMessage

from celery import Celery
from src.config import SMTP_USER, SMTP_PASSWORD

# Default values
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

# Celery - lib for background tasks
# Command to execute celery: celery -A src.tasks.tasks:celery worker --loglevel=INFO
# Command to execute flower (localhost:5555): celery -A src.tasks.tasks:celery flower
celery = Celery('tasks', broker="redis://localhost:6379")


def get_email_template_dashboard(username: str):
    email = EmailMessage()
    email['Subject'] = "Dashboard Report"
    email['From'] = SMTP_USER
    email['To'] = SMTP_USER

    email.set_content(
        "<div>"
        f"<h1>Hello {username}, this is your dashboard report</h1>"
        "</div>",
        subtype='html'
    )

    return email


@celery.task
def send_email_report_dashboard(username: str):
    email = get_email_template_dashboard(username)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)
