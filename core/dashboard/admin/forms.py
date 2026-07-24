from django.contrib.auth import forms as auth_forms
from django import forms 
from django.utils.translation import gettext_lazy as _ 

from accounts.models import Profile
from shop.models import Product 

class AdminPasswordChangeForm(auth_forms.PasswordChangeForm):
    error_messages={
        "password_incorrect":_(
            "پسورد قبلی شما اشتباه وارد شده است . دوباره تلاش کنید ."
        ),
        "password_mismatch":_("دو پسورد های ورودی باهم مطابقت ندارند ..")
    }

class AdminProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields =[
            "image",
            "first_name",
            "last_name",
            "phone_number",
            
        ]

class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=[
            "category","title","slug","image","description","brief_description","stock","status","discount_percent","price","avg_rate"  
        ]
