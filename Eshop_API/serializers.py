from rest_framework import serializers
from Eshop_Product.models import Product

class ProductModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'price', 'brand', 'image', 'timeStamp', 'active')