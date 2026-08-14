from django.shortcuts import render , redirect
from django.views.generic import FormView , TemplateView , View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from order.permissions import HasCustomerAccessPermission,HasCartCustomerPermission
from order.models import UserAddressModel , OrderModel ,OrderItemModel ,CouponModel
from order.forms import CheckOutForm,ApplyCouponForm
from cart.models import CartModel
from cart.cart import CartSession
from decimal import Decimal
from payment.zarinpal_client import ZarinPalSandBox
from payment.models import PayMentModel

class OrderCheckOutView(LoginRequiredMixin,HasCartCustomerPermission,FormView):
    template_name="order/checkout.html"
    form_class=CheckOutForm
    success_url=reverse_lazy("order:completed")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    
    def form_valid(self , form):
       
        user=self.request.user
        cleaned_data=form.cleaned_data
        
        address = cleaned_data['address_id']
        address = UserAddressModel.objects.get(id=address)
        
        
        cart=CartModel.objects.get(user=user)
        coupon=None
        coupon_id = self.request.session.get("user_coupon",None)
        if coupon_id:
            coupon = CouponModel.objects.get(id=coupon_id)
            total_price = cart.calculate_total_price()
            discount = (total_price * Decimal(coupon.discount_percent)) / 100
            total_price -= discount
        else:
            total_price = cart.calculate_total_price()
        
        self.request.session["user_total_price"]=total_price
        order=self.create_order(address , total_price , coupon)

        self.create_order_items(order , cart)
        order.save()

        if coupon:
            coupon.used_by.add(user)

        
        self.clear_cart(cart)

        self.request.session.pop("user_coupon", None)
        self.request.session.pop("user_total_price", None)

        return redirect(self.create_payment(order))      

    
      
    def create_order(self , address , total_price, coupon=None):
        return OrderModel.objects.create(
        user=self.request.user,
        address=address,
        total_price=total_price,
        coupon=coupon
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

    def create_payment(self , order):
        zarinpal = ZarinPalSandBox()
        response = zarinpal.payment_request(order.total_price)
        payment_obj= PayMentModel.objects.create(
            authority_id = response["data"]["authority"],
            amount = order.total_price

        )
        order.payment = payment_obj
        order.save()
        return zarinpal.generate_payment_url(response["data"]["authority"])



          
    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        cart=CartModel.objects.get(user=self.request.user)
        context["addresses"]=UserAddressModel.objects.filter(user=self.request.user)
        context["total_price"]=cart.calculate_total_price()
        context["final_price"]=self.request.session.get(("user_total_price"),cart.calculate_total_price())
        context["total_discount"]= cart.calculate_total_discount()
        context["total_quantity"]=cart.calculate_total_quantity()
        return context




class ApplyCouponView(LoginRequiredMixin,HasCustomerAccessPermission,View):
    template_name="order/checkout.html"
    def post(self , request):
        form=ApplyCouponForm(request.POST,user=request.user)
        if not form.is_valid():
            for error in form.non_field_errors():
                messages.error(request, error)

            for field in form:
                for error in field.errors:
                    messages.error(request, error)
            return redirect("order:checkout")

        coupon=form.cleaned_data.get("coupon")
        if not coupon:
            messages.error(request ,"لطفا کد تخفییف را وارد کنید.")
            return redirect("order:checkout")

        cart=CartModel.objects.get(user=request.user)
        total_price = cart.calculate_total_price()
        discount = (total_price * Decimal(coupon.discount_percent)) / 100
        final_price = total_price - discount
        request.session["user_coupon"]=coupon.id
        self.request.session["user_total_price"]=str(final_price)
        messages.success(request ,"کد تخفیف با موفقیت اعمال شد.")

        return redirect("order:checkout")
 
class DeleteCouponView(LoginRequiredMixin,HasCustomerAccessPermission,View):
    template_name="order/checkout.html"
    def get(self , request):
        cart=CartModel.objects.get(user=self.request.user)
        request.session.pop("user_coupon", None)
        request.session.pop("user_total_price", None)
        return redirect("order:checkout")


class OrderCompleteView(LoginRequiredMixin,HasCustomerAccessPermission,TemplateView):
    
    template_name="order/completed.html"

class OrderFailedView(LoginRequiredMixin,HasCustomerAccessPermission,TemplateView):
    template_name="order/failed.html"
    
 