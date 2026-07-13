from django.shortcuts import render , redirect
from django.urls import reverse_lazy
from django.views.generic import View 
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import UserType

class DashboardHomeView(LoginRequiredMixin,View):
    def dispatch(self , request , *args , **kwargs):
        if request.user.is_authenticated:
            if request.user.type == UserType.customer.value:
                return redirect(reverse_lazy('#'))
            elif request.user.type == UserType.admin.value:
                return redirect(reverse_lazy('#'))
        else:
            return redirect(reverse_lazy('accounts:login'))

        return super().dispatch(request , *args , **kwargs)

