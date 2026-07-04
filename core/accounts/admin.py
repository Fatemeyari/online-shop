from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session

from .models import Profile , PasswordResetToken ,VerificationToken


User=get_user_model()

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model=User
    list_display=("id","email","is_superuser" , "is_active" , "is_verified")
    list_filter=("email","is_superuser" , "is_active" , "is_verified")
    search_fields=("email",)
    ordering=("email",)
    fieldsets = (
        (
            "Authentication",
            {
                "fields": ("email", "password"),
            },
        ),
        (
            "permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_verified",
                ),
            },
        ),
        (
            "group permissions",
            {
                "fields": ("groups", "user_permissions","type"),
            },
        ),
        (
            "important date",
            {
                "fields": ("last_login",),
            },
        ),
    )
    add_fieldsets=(
        (
            None,
            {
                "classes":("wide,"),
                "fields":(
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_verified",
                    "type"
                ),
            },
        ),
    )

@admin.register(Profile)
class CustomProfileAdmin(admin.ModelAdmin):
    list_display=("id" , "user" , "first_name" , "last_name" , "phone_number")
    search_fields=("user" , "first_name" , "last_name" , "phone_number")


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display=("id" , "user" , "is_used","created_time" , "expires_time")
    search_fields=("user__email",)
    list_filter=("user" , "is_used","expires_time")


@admin.register(VerificationToken)
class VerificationTokenAdmin(admin.ModelAdmin):
    list_display=("id" , "user" , "is_used","created_time" , "expires_time")
    search_fields=("user__email",)
    list_filter=("user" , "is_used","expires_time")

class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']
admin.site.register(Session, SessionAdmin)

