from django.shortcuts import render , redirect
from django.urls import reverse_lazy
from django.views.generic import View , TemplateView , UpdateView , ListView , CreateView , DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin 

from dashboard.permissions import HasCustomerAccessPermission
from accounts.models import User , Profile
from dashboard.customer.forms import CustomerPasswordChangeForm ,CustomerProfileEditForm 
from order.models import UserAddressModel 

class CustomerDashboardHomeView(LoginRequiredMixin,HasCustomerAccessPermission,TemplateView):
    template_name="dashboard/customer/home.html"

class CustomSecurityEditView(LoginRequiredMixin,HasCustomerAccessPermission,SuccessMessageMixin,auth_views.PasswordChangeView):
    template_name="dashboard/admin/security_edit.html"
    form_class = CustomerPasswordChangeForm
    success_url = reverse_lazy("dashboard:customer:security-edit")
    success_message= "به روزرسانی پسورد با موفقیت انجام شد."

    def form_invalid(delf , form):
        return super().form_invalid(form)


class CustomProfileEditView(LoginRequiredMixin,HasCustomerAccessPermission,SuccessMessageMixin,UpdateView):
    template_name="dashboard/admin/profile_edit.html"
    form_class = CustomerProfileEditForm
    success_url = reverse_lazy("dashboard:customer:profile-edit")
    success_message= "به روزرسانی پروفایل  با موفقیت انجام شد."

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)


class CustomerAddressListView(LoginRequiredMixin,HasCustomerAccessPermission,ListView):
    template_name="dashboard/customer/address_list.html"

    def get_queryset(self):
        queryset = UserAddressModel.objects.filter(user=self.request.user)
        
        if search_q:= self.request.GET.get("q"):
            queryset = queryset.filter(title__icontains=search_q)

        if search_q := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset

    
