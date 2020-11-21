from Eshop_Product.models import Product
from .serializers import ProductModelSerializer
from rest_framework import viewsets, permissions

class ProductModelSerializer(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    permission_classes = [permissions.IsAdminUser]