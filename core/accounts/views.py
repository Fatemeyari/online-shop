from django.shortcuts import render
from django.contrib.auth import views as auth_views

from .forms import AuthenticationForm

class LoginView(auth_views.LoginView):
    form_class = AuthenticationForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class LogoutView(auth_views.LogoutView):
    pass

