from django.urls import path
from .views import RegistrationView, CustomAuthToken, CustomDiscardToken

app_name = 'account-api-v1'

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('token/login/', CustomAuthToken.as_view(), name='token-login'),
    path('token/logout/', CustomDiscardToken.as_view(), name='token-logout'),
]
