from django.urls import path

from .views import get_active_products

urlpatterns = [
    path('get-active-products', get_active_products.as_view()),
]