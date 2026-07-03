from django.contrib import admin

from .models import ContactUs , NewsLetter

@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display=("fullname" , "email" ,"phone_number" , "is_seen", "created_time")
    search_fields = ("fullname", "email", "phone_number")
    list_filter = ("is_seen", "created_time")
    
@admin.register(NewsLetter)
class NewsLetterAdmin(admin.ModelAdmin):
    list_display=( "email", "created_time")
    search_fields=("email",)







