from django.urls import path
from .views import RegistrationView, CustomAuthToken, CustomDiscardToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

app_name = 'account-api-v1'

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('token/login/', CustomAuthToken.as_view(), name='token-login'),
    path('token/logout/', CustomDiscardToken.as_view(), name='token-logout'),
    path('jwt/create/', TokenObtainPairView.as_view(), name='jwt-create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt-create'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt-create'),

]
