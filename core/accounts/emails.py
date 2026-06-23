from django.core.mail import send_mail
from django.conf import settings

from celery import shared_task
from celery.utils.log import get_task_logger

from .tokens import create_token , create_verification_token
from .models import User


logger=get_task_logger(__name__)

@shared_task
def send_email(user_id):
    user=User.objects.get(id=user_id)
    token=create_token(user)
    token_link=(f"http://127.0.0.1:8000/accounts/password-reset-confirm/{token}")

    send_mail(
        subject="Reset Password Your Account",
        message=f"Click this link to reset your password:\n{token_link}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False

    )


@shared_task
def send_verification_email(user_id):
    user=User.objects.get(id=user_id)
    token=create_verification_token(user)
    token_link=(f"http://127.0.0.1:8000/accounts/signup-confirm/{token}")
    send_mail(
        subject="Verification Your Account",
        message=f"Click this link to verify your account:\n{token_link}",

        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False
    )