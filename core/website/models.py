from django.db import models

from accounts.models import User


class ContactUs(models.Model):
    fullname=models.CharField(max_length=255)
    email=models.EmailField(default=None , null=True)
    phone_number=models.CharField(max_length=13 , blank=True , null=True)
    subject=models.CharField(max_length=255 , null=True , blank=True)
    message=models.TextField(max_length=1000)
    is_seen=models.BooleanField(default=False)
    created_time=models.DateTimeField(auto_now_add=True)
    updated_time=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=["-created_time"]
        verbose_name="Contact Message"
        verbose_name_plural="Contact Messages"

    def __str__(self):
        return self.fullname