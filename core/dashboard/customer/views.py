from django.shortcuts import render , redirect
from django.urls import reverse_lazy
from django.views.generic import View , TemplateView , UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin 

from dashboard.permissions import HasCustomerAccessPermission
from accounts.models import User , Profile
from dashboard.customer.forms import CustomerPasswordChangeForm 

class CustomerDashboardHomeView(LoginRequiredMixin,HasCustomerAccessPermission,TemplateView):
    template_name="dashboard/customer/home.html"

class CustomSecurityEditView(LoginRequiredMixin,HasCustomerAccessPermission,SuccessMessageMixin,auth_views.PasswordChangeView):
    template_name="dashboard/admin/security_edit.html"
    form_class = CustomerPasswordChangeForm
    success_url = reverse_lazy("dashboard:customer:security-edit")
    success_message= "به روزرسانی پسورد با موفقیت انجام شد."

    def form_invalid(delf , form):
        return super().form_invalid(form)






        