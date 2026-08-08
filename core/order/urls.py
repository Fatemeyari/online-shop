from django.urls import path 

from . import views 

app_name="order"

urlpatterns = [
    path("checkout/" , views.OrderCheckOutView.as_view() , name="checkout"),
    path("completed/" , views.OrderCompleteView.as_view() , name="completed"),
    path("applycoupon/" , views.ApplyCouponView.as_view() , name="applycoupon"),
]