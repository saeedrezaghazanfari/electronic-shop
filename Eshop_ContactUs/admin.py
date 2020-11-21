from django.contrib import admin
from Eshop_ContactUs.models import ContactModel, OpinionModel

class ContactAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'timeStamp']

class OpinionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'timeStamp']

admin.site.register(ContactModel, ContactAdmin)
admin.site.register(OpinionModel, OpinionAdmin)