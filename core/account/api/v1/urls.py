from django.urls import path
from .views import RegistrationView, CustomAuthToken

app_name = 'account-api-v1'

urlpatterns = [
    path('registration/',RegistrationView.as_view(),name='registration'),
    path('token/login/',CustomAuthToken.as_view(),name='token-login'),
]


