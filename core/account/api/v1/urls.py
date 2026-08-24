from django.contrib.auth.views import PasswordChangeView
from django.urls import path
from .views import RegistrationView, CustomAuthToken, CustomDiscardToken, CustomTokenObtainPairView, PasswordChangeView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

app_name = 'account-api-v1'

urlpatterns = [
    # registration
    path('registration/', RegistrationView.as_view(), name='registration'),

    # login Token
    path('token/login/', CustomAuthToken.as_view(), name='token-login'),

    # logout
    path('token/logout/', CustomDiscardToken.as_view(), name='token-logout'),

    # login JWT
    path('jwt/create/', CustomTokenObtainPairView.as_view(), name='jwt-create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt-create'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt-create'),

    # password change
    path('password_change/', PasswordChangeView.as_view(), name='password-change'),

]
