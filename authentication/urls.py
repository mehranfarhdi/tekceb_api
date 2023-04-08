from django.urls import path
from authentication import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


app_name = 'user_auth'

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.LogoutAPIView.as_view(), name="logout"),
    path('register/', views.RegisterApi.as_view(), name="register"),
    path('verifycode/', views.VerifyApi.as_view(), name="verify"),
    path('reset_password/', views.ResetPasswordApi.as_view(), name="verify"),
    path('verify_phone/', views.VerifyPhoneApi.as_view(), name="verify"),
    # path('rud/<int:pk>', views.UserRUD.as_view(), name="rud_user"),
]