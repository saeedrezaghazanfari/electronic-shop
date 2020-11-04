from django.shortcuts import render
from .models import SiteSetting

def About_Us_Page(request):
    siteSetting = SiteSetting.objects.first()
    context = {
        'siteSetting':siteSetting
    }
    return render(request, 'About-Us.html', context)