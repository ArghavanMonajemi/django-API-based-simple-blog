from .views import CategoryViewSet, PostViewSet
from rest_framework.routers import DefaultRouter

app_name = 'api-v1'
router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('posts', PostViewSet, basename='post')
urlpatterns = router.urls