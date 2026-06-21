from django.core.mail import send_mail
from django.conf import settings

from celery import shared_task
from celery.utils.log import get_task_logger

from .tokens import create_token
from .models import User


logger=get_task_logger(__name__)

@shared_task
def send_email(user_id):
    user=User.objects.get(id=user_id)
    token=create_token(user)
    token_link=(f"http://127.0.0.1:8000/accounts/password-reset-confirm/{token}")

    send_mail(
        subject="Reset Password Your Account",
        message=f"fClick this link to reset your password:\n{token_link}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False

    )


