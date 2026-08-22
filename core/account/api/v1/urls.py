from django.urls import path
from .views import RegistrationView

app_name = 'account-api-v1'

urlpatterns = [
    path('registration/',RegistrationView.as_view(),name='registration'),
]


