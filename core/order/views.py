from django.shortcuts import render , redirect
from django.views.generic import FormView , TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from order.permissions import HasCustomerAccessPermission
from order.models import UserAddressModel
from order.forms import CheckOutForm
from cart.models import CartModel

class OrderCheckOutView(LoginRequiredMixin,HasCustomerAccessPermission,FormView):
    template_name="order/checkout.html"
    form_class=CheckOutForm
    success_url=reverse_lazy("order:completed")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self , form):
        cleaned_data=form.cleaned_data
        address=cleaned_data['address_id']
        return redirect("order:completed")

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        cart=CartModel.objects.get(user=self.request.user)
        context["addresses"]=UserAddressModel.objects.filter(user=self.request.user)
        context["total_price"]=cart.calculate_total_price()
        context["final_price"]=cart.calculate_total_price()+50000
        context["total_discount"]=cart.calculate_total_discount()
        context["total_quantity"]=cart.calculate_total_quantity()
        return context


class OrderCompleteView(LoginRequiredMixin,HasCustomerAccessPermission,TemplateView):
    template_name="order/completed.html"