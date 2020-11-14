from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.contrib import messages
from Eshop_ContactUs.models import OpinionModel
from Eshop_Other.models import MainSlider, Brands, Notification
from Eshop_Product.models import Product, Category, ProductBrand
from Eshop_AboutUs.models import SiteSetting
from Eshop_ContactUs.forms import OpinionForm
from Eshop_Blog.models import BlogModel
from Eshop_Order.models import OffCode

def Home_Page(request):
    siteSetting = SiteSetting.objects.first()
    latest_pro = Product.objects.all().order_by('-id')[:10]
    mostViews = Product.objects.all().order_by('-views')[:10]
    posts = BlogModel.objects.all().order_by('-id')[:10]

    if request.POST:
        form = OpinionForm(request.POST)
        if request.user.is_authenticated:
            if form.is_valid():
                post_item = form.save(commit=False)
                post_item.save()
                op: OpinionModel = OpinionModel.objects.filter(opinion=form.cleaned_data.get('opinion')).first()
                op.username = f'{request.user.username} - {request.user.email}'
                op.save()

                # send Mail
                subject = 'ارسال نظر'
                from_email = settings.EMAIL_HOST_USER
                to = 'peakabot@gmail.com'
                html_content = f'<div style="border: 1px dashed gray; border-radius: 10px;padding: 20px; margin: 10px 50px; direction: rtl; background: linear-gradient(rgb(203, 203, 248),white, rgb(203, 203, 248));"><h3 style="color: red;">ارسال نظر</h3><p> نام کاربری وارد شده: {op.username} <br>متن نظر: {op.opinion}<br></p></div>'
                msg = EmailMessage(subject, html_content, from_email, [to])
                msg.content_subtype = "html"  # Main content is now text/html
                msg.send()
                messages.info(request, 'نظر، انتقاد و یا پیشنهاد شما برای ما با موفقیت ارسال شد !!')

        else:
            messages.info(request, 'برای ارسال نظر باید وارد سایت شوید.')
            return redirect('/Auth/Login')

    else:
        form = OpinionForm()

    return render(request, 'home.html', {'siteSetting':siteSetting, 'latest_pro':latest_pro, 'mostViews':mostViews, 'form':form, 'posts':posts})

def Slider_partial_Page(requset):
    slides = MainSlider.objects.filter(active=True)
    return render(requset, 'partial_views/slider_partial.html', {'slides': slides})

def Brands_partial_Page(request):
    brands = Brands.objects.filter(active=True).all()
    return render(request, 'partial_views/brands_partial.html', {'brands': brands})

def charts_partial(request):
    products = Product.objects.all().count()
    users = User.objects.all().count()
    blogs = BlogModel.objects.all().count()
    context = {
        'products':products,
        'users':users,
        'blogs':blogs,
    }
    return render(request, 'partial_views/partial_charts.html', context)

def Footer_categories_partail(request):
    category_name = Category.objects.all()[:8]
    context = {
        'categories': category_name
    }
    return render(request, 'partial_views/footer_category.html', context)

def Footer_brands_partail(request):
    brands = ProductBrand.objects.values_list('productBrand', flat=True).distinct()[:8]
    context = {
        'brands': brands
    }
    return render(request, 'partial_views/footer_brands.html', context)

def Header_partial(request):
    notifications = Notification.objects.filter(active=True)
    nav_path = request.META.get("PATH_INFO")
    siteSetting = SiteSetting.objects.first()

    context = {
        'notifications': notifications,
        'nav_path': nav_path,
        'siteSetting':siteSetting,
        'offcode':None
    }

    # Off Code
    offcode = OffCode.objects.filter(active=True).first()
    if offcode:
        context['offcode'] = offcode
    else:
        context['offcode'] = None

    return render(request, 'shared/_header.html', context)

def Footer_partial(request):
    siteSetting = SiteSetting.objects.first()
    context = {
        'siteSetting':siteSetting
    }
    return render(request, 'shared/_footer.html', context)