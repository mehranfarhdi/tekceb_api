from django.urls import path
from authentication import views

app_name = 'user_auth'

urlpatterns = [
    path('register/', views.RegisterApi.as_view(), name="register"),
    path('verifycode/', views.VerifyApi.as_view(), name="verify"),
    path('resetpassword/', views.ResetPasswordApi.as_view(), name="verify"),
    path('verifyphone/', views.VerifyPhoneApi.as_view(), name="verify"),
    path('rud/<int:pk>', views.UserRUD.as_view(), name="rud_user"),
]