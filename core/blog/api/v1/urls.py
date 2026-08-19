from django.urls import path
from rest_framework.routers import DefaultRouter

app_name = 'blog-api-v1'
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
urlpatterns = router.urls