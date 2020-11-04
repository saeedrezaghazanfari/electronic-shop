from django.urls import path
from .views import (
    Product_List_Page,
    Product_Details_Page,
    add_favorites,
    category_partial,
    brand_partial,
    Search_Category,
    Search_Brands,
    Search_Price,
    search_Product_nameBrandTag
)

urlpatterns = [
    path('List', Product_List_Page.as_view()),
    path('Search', search_Product_nameBrandTag.as_view()),
    path('Details/<int:Product_ID>/<str:Product_title>', Product_Details_Page),
    path('Add-to-favorites', add_favorites, name='add_favorites'),
    path('Search/Category/<str:product_category>', Search_Category.as_view()),
    path('Search/Brands/<str:product_brand>', Search_Brands.as_view()),
    path('Search/Price', Search_Price),

    # Partials Views
    path('category-partial', category_partial, name='category_partial'),
    path('brand-partial', brand_partial, name='brand_partial')
]