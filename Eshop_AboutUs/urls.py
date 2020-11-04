from django.urls import path

from Eshop_AboutUs.views import About_Us_Page

urlpatterns = [
    path('About-Us', About_Us_Page)
]