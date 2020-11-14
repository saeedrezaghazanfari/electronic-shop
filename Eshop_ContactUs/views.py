from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from Eshop_AboutUs.models import SiteSetting
from .forms import ContactForm
from .models import ContactModel

def ContactUs_Page(request):
    Contactform = ContactForm(request.POST or None)
    context = {
        'siteSetting':None,
        'Contactform':Contactform
    }
    if request.POST:
        if request.user.is_authenticated:
            if Contactform.is_valid():
                email = Contactform.cleaned_data.get('email')
                name = Contactform.cleaned_data.get('name')
                subject = Contactform.cleaned_data.get('subject')
                msg = Contactform.cleaned_data.get('msg')

                ContactModel.objects.create(name=name, email=email, subject=subject, msg=msg)

                # send Mail
                subjectmail = 'ارسال پیام کاربر سایت'
                from_email = settings.EMAIL_HOST_USER
                to = 'peakabot@gmail.com'
                html_content = f'<div style="border: 1px dashed gray; border-radius: 10px;padding: 20px; margin: 10px 50px; direction: rtl; background: linear-gradient(rgb(203, 203, 248),white, rgb(203, 203, 248));"><h3 style="color: red;">ارسال پیام از کاربر سایت</h3><p>نام: {name}<br>ایمیل: {email}<br>عنوان پیام: {subject}<br>متن پیام: {msg}<br></p></div>'
                msgemail = EmailMessage(subjectmail, html_content, from_email, [to])
                msgemail.content_subtype = "html"                          # Main content is now text/html
                msgemail.send()

                messages.info(request, 'ارسال پیام شما موفقیت بود! در اولین فرصت بررسی میشود.')
                return redirect('/Contact-Us')
        else:
            messages.info(request, 'برای ارسال پیام باید به سیستم وارد شوید.')
            return redirect('/Auth/Login')

    siteSetting = SiteSetting.objects.first()
    context['siteSetting'] = siteSetting

    return render(request, 'contactus.html', context)