from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('', views.ProductModelSerializer)


urlpatterns = [
    path('v1/', include(router.urls)),
]