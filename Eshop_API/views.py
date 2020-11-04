# from django.contrib import messages
# from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Eshop_Product.models import Product
from .serializers import ProductModelSerializer


class get_active_products(APIView):
    def get(self, request):

        # if not request.user.is_superuser:
        #     messages.info(request, 'شما باید اجازه ی دسترسی به API ها را از مدیر سایت بگیرید.')
        #     return redirect('/')

        query = Product.objects.filter(active=True).all()
        serializers = ProductModelSerializer(query, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
