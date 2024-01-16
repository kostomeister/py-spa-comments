import os

from celery import shared_task, Celery
from django.core.mail import send_mail
from django.utils import timezone

from dotenv import load_dotenv

from .models import Comment

load_dotenv()

app = Celery("tasks", backend="redis://localhost", broker="redis://localhost")


@shared_task
def count_comments_and_send_email():
    today = timezone.now().date()
    count = Comment.objects.filter(created_at__date=today).count()

    subject = 'Daily Comment Count'
    message = f'There were {count} comments posted today.'
    from_email = os.environ.get("SENDER_EMAIL")
    to_emails = [os.environ.get("RECEIVER_EMAIL")]

    send_mail(subject, message, from_email, to_emails)
