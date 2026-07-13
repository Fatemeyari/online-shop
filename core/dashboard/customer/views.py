from django.shortcuts import render , redirect
from django.urls import reverse_lazy
from django.views.generic import View , TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from dashboard.permissions import HasCustomerAccessPermission
from accounts.models import User

class CustomerDashboardHomeView(LoginRequiredMixin,HasCustomerAccessPermission,TemplateView):
    template_name="dashboard/customer/home.html"

