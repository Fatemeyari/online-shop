from django.core.mail import send_mail
from django.conf import settings

from .tokens import create_token
from .models import PasswordResetToken

def send_email(user):
    token=create_token(user)
    token_link=(f"http://127.0.0.1:8000/accounts/password-reset-confirm/{token}")

    send_mail(
        subject="Reset Password Your Account",
        message=f"fClick this link to reset your password:\n{token_link}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False

    )


