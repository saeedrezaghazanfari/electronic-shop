from django.contrib import admin
from Eshop_Product.models import (
    Product,
    Tag,
    Category,
    ProductGallery,
    ProductVeiw,
    Favorites,
    ProductBrand,
    ProductColor,
    Chart
)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'price', 'jimage', 'active', 'brand', 'categories_to_str', 'jtimeStamp']
    list_editable = ['price', 'active']
    search_fields = ['title', 'price', 'brand']
    ordering = ['-id']

    def categories_to_str(self, obj):
        return ", ".join([category.title for category in obj.categories.all()])
    categories_to_str.short_description = 'دسته بتدی ها'

admin.site.site_header = "فروشگاه لوازم خانگی"

admin.site.register(Product, ProductAdmin)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(ProductGallery)
admin.site.register(ProductVeiw)
admin.site.register(Favorites)
admin.site.register(ProductBrand)
admin.site.register(ProductColor)
admin.site.register(Chart)