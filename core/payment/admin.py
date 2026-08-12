from django.contrib import admin

from .models import PayMentModel 

@admin.register(PayMentModel)
class PayMentAdmin(admin.ModelAdmin):
    list_display=(
        "id",
        "authority_id" ,
        "ref_id" ,
        "amount" ,
        "response_json" ,
        "response_code",
        "status",
        "updated_time",
        "created_time"
        )
