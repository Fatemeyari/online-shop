from django.urls import path , include

from . import views 

app_name ='customer'

urlpatterns = [
   path('home/' , views.CustomerDashboardHomeView.as_view() , name="home"),
   path('security-edit/' , views.CustomSecurityEditView.as_view() , name="security-edit"),
   path('profile-edit/' , views.CustomProfileEditView.as_view() , name="profile-edit"),
   path('address/list/',views.CustomerAddressListView.as_view() , name="address-list"),
   path('address/create/',views.CustomerAddressCreateView.as_view() , name="address-create"),
   path('address/<int:pk>/edit/',views.CustomerAddressEditView.as_view() , name="address-edit"),
   path('address/<int:pk>/delete/',views.CustomerAddressDeleteView.as_view() , name="address-delete"),
   path('success-order-list/',views.CustomerSuccessOrderListView.as_view() , name="success-order-list"),
   path('failed-order-list/',views.CustomerFailedOrderListView.as_view() , name="failed-order-list"),
   path('order/<int:pk>/detail/', views.CustomerOrderDetailView.as_view() , name="order-detail" )


]