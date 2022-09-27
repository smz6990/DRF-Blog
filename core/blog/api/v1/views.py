from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from ...models import Post, Category
from .serializers import PostSerializer, CategorySerializer
from .permissions import IsOwnerOrReadOnly
from .paginations import CustomPagination


class BlogIndexListCreateAPIView(generics.ListCreateAPIView):
    """
    Class that show the list of all published posts or create new post in API.
    """

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["author", "category"]
    search_fields = ["title", "content"]
    ordering_fields = ["published_date"]
    pagination_class = CustomPagination


class BlogSingleRetrieveUpdateDeleteAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    """
    Class that retrieve a single published post or update or delete it in API.
    """

    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    """
    Class that show the list of all Categories or create new Category in API.
    """

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["name"]
    search_fields = ["name"]
