from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin
from django.dispatch import receiver
from django.db.models.signals import post_save

from accounts.validators import validation_iranian_cellphone
class UserType(models.IntegerChoices):
    customer=1 ,_("customer")
    admin=2 ,_("admin")
    superuser=3 ,_("superuser")


class UserManager(BaseUserManager):
    def create_user(self,email,password , **extra_fields):
        if not email:
            raise ValueError("Please Enter Your Email.")
        email=self.normalize_email(email=email)
        user=self.model(email=email , **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email , password , **extra_fields):
        extra_fields.setdefault("is_staff" , True)
        extra_fields.setdefault("is_superuser" , True)
        extra_fields.setdefault("is_active" , True)
        extra_fields.setdefault("is_verified" , True)
        extra_fields.setdefault("type" , UserType.customer.value)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("superuser must have is_superuser=True")
        return self.create_user(email , password , **extra_fields)



class User(AbstractBaseUser ,PermissionsMixin):
    email=models.EmailField(_("Email Address") , unique=True)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_verified=models.BooleanField(default=False)
    type=models.IntegerField(choices=UserType.choices , default=UserType.customer.value)
    created_time=models.DateTimeField(auto_now_add=True)
    updated_time=models.DateTimeField(auto_now=True)

    USERNAME_FIELD="email"
    REQUIRED_FIELDS=[]

    objects=UserManager()

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name="User"
        verbose_name_plural="Users"


class Profile(models.Model):
    user=models.OneToOneField('User' , on_delete=models.CASCADE , related_name="user_profile")
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    phone_number=models.CharField(max_length=12 , validators=[validation_iranian_cellphone])
    image=models.ImageField(upload_to="profile/")
    created_time=models.DateTimeField(auto_now_add=True)
    updated_time=models.DateTimeField(auto_now=True)

    def get_fullname(self):
        if self.first_name or self.last_name:
            return self.first_name + " " + self.last_name
        return "New User"
    
    class Meta:
        verbose_name="Profile"
        verbose_name_plural="Profiles"


@receiver(post_save , sender=User)
def create_profile(sender , instance , created , **kwarge):
    if created :
        Profile.objects.create(user=instance , pk=instance.pk)