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

class PasswordResetConfirmForm(forms.Form):
    password1 = forms.CharField(
        required=True,
        label="Password",
        widget=forms.PasswordInput(attrs={
            "placeholder": "رمز عبور جدید"
        })
    )

    password2 = forms.CharField(
        required=True,
        label="Confirm_Password",
        widget=forms.PasswordInput(attrs={
            "placeholder": "تکرار رمز عبور"
        })
    )

class SignUpForm(forms.Form):
    email=forms.EmailField(required=True,
                           label="email",
                           widget=forms.EmailInput(attrs={"placeholder":"example@gmail.com"}))
    password1=forms.CharField(required=True , 
                              label="password1",
                              widget=forms.PasswordInput(attrs={"placeholder":"رمز عبور"}))
    
    password2=forms.CharField(required=True,
                              label="password2",
                              widget=forms.PasswordInput(attrs={"placeholder":"تکرار رمز عبور"}))
    
    def clean(self):
        cleaned_data=super().clean()
        password1=cleaned_data.get("password1")
        password2=cleaned_data.get("password2")
        if password1 and password2 and password1 != password2 :
            raise forms.ValidationError("رمز های وارد شده یکسان نیستند.")
        return cleaned_data
 
