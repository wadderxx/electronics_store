from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Product
from .serializers import ProductSerializer
from .filters import ProductFilter
from .permissions import IsAdminOrReadOnly


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]

    search_fields = ['name', 'description']
    filterset_class = ProductFilter

    ordering_fields = ['name', 'price', 'stock', 'created_at']
