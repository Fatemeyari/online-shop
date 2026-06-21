from django.contrib.auth import forms as auth_forms
from django import forms
from django.core.exceptions import ValidationError

class AuthenticationForm(auth_forms.AuthenticationForm):
    def confirm_login_allowed(self, user):
        super(AuthenticationForm,self).confirm_login_allowed(user)

class PasswordResetRequestForm(forms.Form):
    email=forms.EmailField(required=True,
                          label="email",
                          widget=forms.EmailInput(attrs={"placeholder": "example@gmail.com"}))

                    

