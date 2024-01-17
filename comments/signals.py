import os

from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from dotenv import load_dotenv

from comments.models import Comment

load_dotenv()


@receiver(post_save, sender=Comment)
def send_borrow_message_admin(sender, instance, created, **kwargs):
    if created and instance.parent is not None:
        subject = f'Re: Your Comment on {instance.parent.created_at}'
        message = f"Hello {instance.parent.username},\n\n" \
                  f"Someone has replied to your comment:\n\n" \
                  f"{instance.text}\n\n" \
                  f"Best regards,\nYour Website Team"
        from_email = os.environ.get("SENDER_EMAIL")
        to_email = instance.parent.email

        print(from_email, to_email)

        send_mail(subject, message, from_email, [to_email])
