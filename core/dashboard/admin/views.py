from django.shortcuts import render , redirect
from django.urls import reverse_lazy
from django.views.generic import View , TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin 

from dashboard.permissions import HasAdminAccessPermission
from accounts.models import User
from dashboard.admin.forms import AdminPasswordChangeForm

class AdminDashboardHomeView(LoginRequiredMixin,HasAdminAccessPermission,TemplateView):
    template_name="dashboard/admin/home.html"


class AdminSecurityEditView(LoginRequiredMixin,HasAdminAccessPermission,SuccessMessageMixin,auth_views.PasswordChangeView):
    template_name="dashboard/admin/security_edit.html"
    form_class = AdminPasswordChangeForm
    success_url = reverse_lazy("dashboard:admin:security-edit")
    success_message= "به روزرسانی پسورد با موفقیت انجام شد."

    def form_invalid(delf , form):
        print(form.errors)
        return super().form_invalid(form)



        