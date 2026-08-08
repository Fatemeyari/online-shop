from django.urls import path , include

from . import views 

app_name ='admin'

urlpatterns = [
   path('home/' , views.AdminDashboardHomeView.as_view() , name="home"),
   path('security-edit/' , views.AdminSecurityEditView.as_view() , name="security-edit"),
   path('profile-edit/' , views.AdminProfileEditView.as_view() , name="profile-edit"),
   path('product-list/' , views.AdminProductListView.as_view() , name="product-list"),
   path('product/<int:pk>/detail/' , views.AdminProductEditView.as_view() , name="product-edit"),
   path('product/<int:pk>/delete/' , views.AdminProductDeleteView.as_view() , name="product-delete"),
   path('product-create/' , views.AdminProductCreateView.as_view() , name="product-create"),
   path('coupon-list/' , views.CouponListView.as_view() , name="coupon-list"),


  
]