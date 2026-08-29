from django.contrib import admin
from .models import ReviewModel
# Register your models here.


@admin.register(ReviewModel)
class ReviewModelModelAdmin(admin.ModelAdmin):
    list_display =("id","user","product","rate","created_time")