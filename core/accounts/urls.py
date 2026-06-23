from django.urls import path

from accounts import views
app_name="accounts"


urlpatterns = [
    path('login/' ,views.LoginView.as_view() , name="login"),
    path('logout/' ,views.LogoutView.as_view() , name="logout"),
    path('password-reset-request/' , views.PasswordResetRequestView.as_view() , name="password-reset-request"),
    path('password-reset-confirm/<str:token>' , views.PasswordResetConfirmView.as_view() , name="password-reset-confirm"),
    path('signup/' , views.SignUpView.as_view() , name="signup" ),
    path('signup-confirm/<str:token>/' , views.SignupConfirmView.as_view() , name="signup-confirm" ),
    path('resend_verification/' , views.ResendVerificationView.as_view() , name="resend_verification" ),





]
