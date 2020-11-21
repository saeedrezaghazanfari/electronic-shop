from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from Eshop_Auth.models import UltraProfile, ReportSpam_Model
# from django.contrib.auth.models import User


# admin.site.register(User, UserAdmin)
admin.site.register(UltraProfile)
admin.site.register(ReportSpam_Model)
