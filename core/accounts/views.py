from django.shortcuts import render ,redirect
from django.http import HttpResponse
from django.contrib.auth import views as auth_views
from django.views import View
from django.contrib import messages
from django.utils import timezone

from .forms import AuthenticationForm , PasswordResetRequestForm , PasswordResetConfirmForm
from .models import User , PasswordResetToken
from .emails import send_email

class LoginView(auth_views.LoginView):
    form_class = AuthenticationForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class LogoutView(auth_views.LogoutView):
    pass


class PasswordResetRequestView(View):
    template_name="accounts/password_reset_request.html"

    def get(self,request):
        form=PasswordResetRequestForm()
        return render(request , self.template_name,{"form":form})

    def post(self , request):
        form=PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data["email"]
            try:
                user=User.objects.get(email=email)
            except User.DoesNotExist:
                form.add_error("email","کاربری با این ایمیل یافت نشد .")
                return render(request, self.template_name, {"form": form})

        send_email(user)
        messages.success(request,"ایمیل بازیابی ارسال شد.")
        return render(request , self.template_name , {"form":form})


class PasswordResetConfirmView(View):
    template_name = "accounts/password_reset_confirm.html"

    def get(self, request, token):
        form = PasswordResetConfirmForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, token):
        form = PasswordResetConfirmForm(request.POST)
        try:
            token_obj = PasswordResetToken.objects.get(token=token)
        except PasswordResetToken.DoesNotExist:
            form.add_error(None, ".توکن نامعتبر است")
            return render(request, self.template_name, {"form": form})

        if token_obj.is_used:
            form.add_error(None, ".این توکن قبلاً استفاده شده است.")
            return render(request, self.template_name, {"form": form})

        if token_obj.expires_time < timezone.now():
            form.add_error(None, ".این توکن منقضی شده است.")
            return render(request, self.template_name, {"form": form})

        if form.is_valid():
            password = form.cleaned_data["password1"]
            user = token_obj.user
            user.set_password(password)
            user.save()

            token_obj.is_used = True
            token_obj.save()

            messages.success(request, ".پسورد با موفقیت تغییر یافت.")
            return redirect("login")  
        return render(request, self.template_name, {"form": form})