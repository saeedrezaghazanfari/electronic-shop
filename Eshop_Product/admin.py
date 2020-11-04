from django.contrib import admin
from Eshop_Product.models import Product, Tag, Category, ProductGallery, ProductVeiw, Favorites, ProductBrand, ProductColor

class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'price', 'active', 'brand', 'timeStamp']
    list_editable = ['price', 'active']
    search_fields = ['title', 'price', 'brand']

admin.site.register(Product, ProductAdmin)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(ProductGallery)
admin.site.register(ProductVeiw)
admin.site.register(Favorites)
admin.site.register(ProductBrand)
admin.site.register(ProductColor)