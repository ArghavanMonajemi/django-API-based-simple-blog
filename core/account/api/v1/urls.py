from django.urls import path
from .views import RegistrationView, CustomAuthToken, CustomDiscardToken, CustomTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

app_name = 'account-api-v1'

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('token/login/', CustomAuthToken.as_view(), name='token-login'),
    path('token/logout/', CustomDiscardToken.as_view(), name='token-logout'),
    path('jwt/create/', CustomTokenObtainPairView.as_view(), name='jwt-create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt-create'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt-create'),

]
