from django.urls import path

from Eshop_ContactUs.views import ContactUs_Page

urlpatterns = [
    path('Contact-Us', ContactUs_Page),
]