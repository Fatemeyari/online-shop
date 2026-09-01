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
   path('coupon-create/' , views.CouponCreateView.as_view() , name="coupon-create"),
   path('coupon/<int:pk>/detail/', views.CouponEditView.as_view() , name="coupon-edit"),
   path('coupon/<int:pk>/delete/' , views.CouponDeleteView.as_view() , name="coupon-delete"),
   path('success-order-list/' , views.AdminSuccessOrderListView.as_view() , name="success-order-list"),
   path('failed-order-list/',views.AdminFailedOrderListView.as_view() , name="failed-order-list"),
   path('order/<int:pk>/detail/', views.AdminOrderDetailView.as_view() , name="order-detail" ),
   path('order/<int:pk>/invoice/' , views.AdminOrderInvoiceView.as_view() , name="order-invoice"),
   path('review-list/' , views.AdminReviewListView.as_view() , name="review-list"),
   path('review/<int:pk>/detail/',views.AdminReviewEditView.as_view() , name="review-detail")


  
]