from django.shortcuts import render , redirect
from django.views.generic import FormView , TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from order.permissions import HasCustomerAccessPermission
from order.models import UserAddressModel , OrderModel ,OrderItemModel ,CouponModel
from order.forms import CheckOutForm
from cart.models import CartModel
from cart.cart import CartSession
from decimal import Decimal


class OrderCheckOutView(LoginRequiredMixin,HasCustomerAccessPermission,FormView):
    template_name="order/checkout.html"
    form_class=CheckOutForm
    success_url=reverse_lazy("order:completed")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self , form):
        print("FORM VALID RUN")
        print(form.cleaned_data)
        action=self.request.POST.get("action")
        
        user=self.request.user
        cleaned_data=form.cleaned_data

        address = cleaned_data['address_id']
        address = UserAddressModel.objects.get(id=address)
        
        
        cart=CartModel.objects.get(user=user)
        total_price = cart.calculate_total_price()

        order=self.create_order(address , total_price)

        self.create_order_items(order , cart)

        order.save()

        self.clear_cart(cart)

        return redirect("order:completed")
     
 
        
      
    def create_order(self , address , total_price):
        return OrderModel.objects.create(
        user=self.request.user,
        address=address,
        total_price=total_price
        )

    def create_order_items(self,order , cart):
        for item in cart.cart_items.all():
            OrderItemModel.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.get_price(),
            )


    def clear_cart(self , cart):
        cart.cart_items.all().delete()
        CartSession(self.request.session).clear()
          
    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        cart=CartModel.objects.get(user=self.request.user)
        context["addresses"]=UserAddressModel.objects.filter(user=self.request.user)
        context["total_price"]=cart.calculate_total_price() 
        context["total_discount"]= cart.calculate_total_discount()
        context["total_quantity"]=cart.calculate_total_quantity()

        return context


class OrderCompleteView(LoginRequiredMixin,HasCustomerAccessPermission,TemplateView):
    template_name="order/completed.html"