import secrets
from datetime import timedelta

from django.utils import timezone
from .models import PasswordResetToken , VerificationToken



def invalidate_user_token(user):
    PasswordResetToken.objects.filter(user=user , is_used=False).update(is_used=True)



def create_token(user):
    invalidate_user_token(user)
    token=secrets.token_urlsafe(32)
    expires_time=timezone.now() + timedelta(hours=48)
    PasswordResetToken.objects.create(
        user=user,
        token=token,
        is_used=False,
        expires_time=expires_time,
    )
    return token




def invalidate_user_verification_token(user):
    VerificationToken.objects.filter(user=user , is_used=False).update(is_used=True)


def create_verification_token(user):
    invalidate_user_verification_token(user)
    token=secrets.token_urlsafe(32)
    expires_time=timezone.now() + timedelta(hours=24)
    VerificationToken.objects.create(
        user=user,
        token=token,
        is_used=False,
        expires_time=expires_time
    )
    return token
