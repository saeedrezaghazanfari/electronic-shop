from django.contrib import admin

from Eshop_Order.models import Order, OrderDetails, OffCode

admin.site.register(Order)
admin.site.register(OrderDetails)
admin.site.register(OffCode)