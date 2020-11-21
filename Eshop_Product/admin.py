from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext

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

    def all_off(self, request, queryset):
        updated = queryset.update(is_off=True)
        self.message_user(request, ngettext(
            '%d تخفیف داده شد.',
            '%d تخفیف داده شدند.',
            updated,
        ) % updated, messages.SUCCESS)
    all_off.short_description = "همگی تخفیف داده شوند"

    def all_no_off(self, request, queryset):
        updated = queryset.update(is_off=False)
        self.message_user(request, ngettext(
            '%d تخفیف برداشته شد.',
            '%d تخفیف برداشته شدند.',
            updated,
        ) % updated, messages.SUCCESS)
    all_no_off.short_description = "همگی تخفیف داده نشوند"

    list_display = ['__str__', 'price', 'jimage', 'active', 'brand', 'categories_to_str', 'jtimeStamp', 'is_off']
    list_editable = ['price', 'active']
    search_fields = ['title', 'price', 'brand']
    ordering = ['-id']
    actions = [all_off, all_no_off]

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