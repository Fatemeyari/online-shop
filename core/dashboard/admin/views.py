from django.shortcuts import render , redirect
from django.urls import reverse_lazy
from django.views.generic import View , TemplateView , UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin 

from dashboard.permissions import HasAdminAccessPermission
from accounts.models import User , Profile
from dashboard.admin.forms import AdminPasswordChangeForm ,AdminProfileEditForm

class AdminDashboardHomeView(LoginRequiredMixin,HasAdminAccessPermission,TemplateView):
    template_name="dashboard/admin/home.html"


class AdminSecurityEditView(LoginRequiredMixin,HasAdminAccessPermission,SuccessMessageMixin,auth_views.PasswordChangeView):
    template_name="dashboard/admin/security_edit.html"
    form_class = AdminPasswordChangeForm
    success_url = reverse_lazy("dashboard:admin:security-edit")
    success_message= "به روزرسانی پسورد با موفقیت انجام شد."

    def form_invalid(delf , form):
        return super().form_invalid(form)


class AdminProfileEditView(LoginRequiredMixin,HasAdminAccessPermission,SuccessMessageMixin,UpdateView):
    template_name="dashboard/admin/profile_edit.html"
    form_class = AdminProfileEditForm
    success_url = reverse_lazy("dashboard:admin:profile-edit")
    success_message= "به روزرسانی پروفایل  با موفقیت انجام شد."

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)






        