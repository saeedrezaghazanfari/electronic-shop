from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    Home_Page,
    Slider_partial_Page,
    Brands_partial_Page,
    Footer_categories_partail,
    Footer_brands_partail,
    Header_partial, Footer_partial,
    charts_partial,
)

urlpatterns = [
    path('Product/', include('Eshop_Product.urls')),
    path('', include('Eshop_Auth.urls')),
    path('', include('Eshop_ContactUs.urls')),
    path('', include('Eshop_AboutUs.urls')),
    path('Blog/', include('Eshop_Blog.urls')),
    path('user/', include('Eshop_PannelUser.urls')),
    path('api/', include('Eshop_API.urls')),
    path('', include('Eshop_Order.urls')),

    path('', Home_Page),
    path('mainSlider-Partial', Slider_partial_Page, name="Slider_partial_Page"),
    path('Brands-Partial', Brands_partial_Page, name="Brands_partial_Page"),
    path('footer-category-Partial', Footer_categories_partail, name="Footer_categories_partail"),
    path('footer-brand-Partial', Footer_brands_partail, name="Footer_brands_partail"),
    path('Header-partial', Header_partial, name="Header_partial"),
    path('Footer-partial', Footer_partial, name="Footer_partial"),
    path('charts-partial', charts_partial, name="charts_partial"),
    re_path(r'^ratings/', include('star_ratings.urls', namespace='ratings')),

    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('secret/administrator/pages/admin/', admin.site.urls , name="adminpage"),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)