from django.urls import path , include

from . import views 

app_name ='customer'

urlpatterns = [
   path('home/' , views.CustomerDashboardHomeView.as_view() , name="home"),
   path('security-edit/' , views.CustomSecurityEditView.as_view() , name="security-edit"),
   path('profile-edit/' , views.CustomProfileEditView.as_view() , name="profile-edit"),
   path('address/list/',views.CustomerAddressListView.as_view() , name="address-list"),
   path('address/create/',views.CustomerAddressCreateView.as_view() , name="address-create"),
   

]