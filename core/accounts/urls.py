from django.urls import path

from accounts import views
app_name="accounts"


urlpatterns = [
    path('login/' ,views.LoginView.as_view() , name="login"),
    path('logout/' ,views.LogoutView.as_view() , name="logout"),
    path('password-reset-request/' , views.PasswordResetRequestView.as_view() , name="password-reset-request"),

]
