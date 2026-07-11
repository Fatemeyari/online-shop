from django.shortcuts import render, redirect
from django.views.generic import View ,TemplateView

from django.http import JsonResponse

from shop.models import Product ,ProductStatusType
from .cart import CartSession
# Create your views here.

class SessionAddProduct(View):
    def post(self,request,*args, **kwargs):
        cart=CartSession(request.session)
        product_id=request.POST.get("product_id")
        print(product_id)
        if product_id and Product.objects.filter(id=product_id , status=ProductStatusType.publish.value).exists():
            cart.add_product(product_id)
        return redirect(request.META.get("HTTP_REFERER", "/"))        

class DecreaseProductQuantityView(View):
    def post(self,request , *args , **kwargs):
        cart=CartSession(request.session)  
        product_id=request.POST.get("product_id")
        if product_id:
            cart.decrease_product_quantity(product_id)
        return redirect(request.META.get("HTTP_REFERER","/"))

class IncreaseProductQuantityView(View):
    def post(self,request , *args , **kwargs):
        cart=CartSession(request.session)  
        product_id=request.POST.get("product_id")
        if product_id:
            cart.increase_product_quantity(product_id)
        return redirect(request.META.get("HTTP_REFERER","/"))
    
class CartSummaryView(TemplateView):
    template_name="cart/cart_summary.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart=CartSession(self.request.session)
        context["cart_items"]=cart.get_cart_items()
        context["total_price"]=cart.get_total_price()
        context["total_quantity"]=cart.get_total_quantity()
        context["discounts"]=cart.get_discount()
        return context  

  