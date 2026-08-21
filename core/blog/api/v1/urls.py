from django.urls import path
from .views import CategoryViewSet, PostViewSet
from rest_framework.routers import DefaultRouter

app_name = 'blog-api-v1'
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'posts', PostViewSet, basename='post')
urlpatterns = router.urls