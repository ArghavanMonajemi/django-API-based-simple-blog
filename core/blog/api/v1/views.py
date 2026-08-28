from blog.models import Post, Category
from .serializer import CategorySerializer, PostSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from .paginations import StandardCursorPagination
from .permissions import IsOwnerOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["name"]
    ordering_fields = ["name"]
    search_fields = ["name"]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(status=1)
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["title", "category", "author"]
    ordering_fields = ["pub_date"]
    search_fields = ["title", "author"]
    pagination_class = StandardCursorPagination
