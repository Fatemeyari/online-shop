from django import forms
from django.core.exceptions import ValidationError

from .models import ContactUs

class ContactForm(forms.ModelForm):
    class Meta:
        model=ContactUs
        fields=("fullname" , "email" , "phone_number" , "subject" , "message")
        error_massages={
            'fullname':
            {
              'required':'فیلد نام و نام خانوادگی نمی تواند خالی باشد .'  
            },
            'email':{
                'required':'فیلد ایمیل نمی تواند خالی باشد .'  
            },
            'subject':{
                'required':'فیلد عنوان نمی تواند خالی باشد .'  
            },
            'message':{
                'required':'فیلد عنوان نمی تواند خالی باشد .'  ,
                'max_length': 'محتوای نوشته شده بیشتر از حد مجاز است .'
            }
        }