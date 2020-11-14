from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm, Report_Spam
from django.contrib import messages
from .models import ReportSpam_Model, UltraProfile
from Eshop_Other.models import Send_Notifications_email_Model
from django.conf import settings
from django.core.mail import EmailMessage
from Eshop_AboutUs.models import SiteSetting

def Login_Page(request):
    if request.user.is_authenticated:
        messages.info(request, 'شما در حال حاضر دارای یک حساب کاربری میباشید.')
        return redirect('/')

    loginForm = LoginForm(request.POST or None)
    context = {
        'loginForm': loginForm,
    }
    if loginForm.is_valid():
        email = loginForm.cleaned_data.get('email')
        password = loginForm.cleaned_data.get('password')

        convert: User = User.objects.filter(email__iexact=email).first()
        if convert:
            user = authenticate(request, username=convert.username, password=password)
            if user:
                login(request, user)
                context['loginForm'] = LoginForm()
                return redirect('/Auth/pre-home')
        else:
            loginForm.add_error('email', 'اکانتی با این ایمیل وجود ندارد.')

    return render(request, 'login_page.html', context)

def Logout_Page(request):
    if not request.user.is_authenticated:
        messages.info(request, 'شما در حال حاضر داخل سیستم نیستید !!')
        return redirect('/Auth/Login')

    logout(request)
    messages.info(request, 'خروج شما از سیستم موفقیت بود !!')
    return redirect('/Auth/Login')

def Register_Page(request):
    if request.user.is_authenticated:
        messages.info(request, 'شما نمیتوانید زمانی که داخل سیستم هستید ، اکانت دیگری راه اندازی کنید !!')
        return redirect('/')

    registerForm = RegisterForm(request.POST or None)
    context = {
        'register': registerForm
    }
    if registerForm.is_valid():
        username = registerForm.cleaned_data.get('username')
        email = registerForm.cleaned_data.get('email')
        password = registerForm.cleaned_data.get('password')
        User.objects.create_user(username=username, email=email, password=password)
        context['register'] = RegisterForm()

        nameEshop: SiteSetting = SiteSetting.objects.last()
        user = User.objects.get(username__iexact=username)

        # send Mail
        subject = f'به فروشگاه الکترونیکی {nameEshop.App_Name} خوش آمدید!!'
        from_email = settings.EMAIL_HOST_USER
        to = user.email
        html_content = f'<div style="border: 1px dashed gray; border-radius: 10px;padding: 20px; margin: 10px 50px; direction: rtl; background: linear-gradient(rgb(203, 203, 248),white, rgb(203, 203, 248));"><h3 style="color: red;">به وبسایت <span style="color: blue; font-weight: 900;">{nameEshop.App_Name}</span> خوش آمدید!!</h3><p>با عرض سلام و درود،	<br> عضویت شما در سایت ما با موفقیت انجام شد. شما برای ورود باید در این <a href="http://127.0.0.1:8000/Auth/Login" style="color: blue; text-decoration: none;">صفحه</a> اطلاعات خود را وارد کنید. </p></div>'
        msg = EmailMessage(subject, html_content, from_email, [to])
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()

        messages.info(request,'ساخت اکانت شما موفقیت بود ، برای ورود به سیستم اطلاعات خود را وارد کنید.')
        return redirect('/Auth/Login')

    return render(request, 'register_page.html', context)

def pre_home_page(request):
    if not Send_Notifications_email_Model.objects.filter(user_id=request.user.id).first():
        Send_Notifications_email_Model.objects.create(user_id=request.user.id , activeSend=True)

    if not UltraProfile.objects.filter(user_id=request.user.id).first():
        UltraProfile.objects.create(user_id=request.user.id, phone=0, webName='', bio='')
    messages.info(request, 'ورود شما به سیستم موفقیت بود !!')
    return redirect('/')

@login_required(login_url='/Auth/Login')
def report_spam(request):
    report_spam = Report_Spam(request.POST or None, initial={'username':request.user.username, 'email':request.user.email})
    context = {
        'report': report_spam
    }
    if report_spam.is_valid():
        subject = report_spam.cleaned_data.get('subject')
        massage = report_spam.cleaned_data.get('massage')
        username = report_spam.cleaned_data.get('username')
        email = report_spam.cleaned_data.get('email')
        imageErr = request.FILES.get('imageErr')
        ReportSpam_Model.objects.create(email=email, username=username, subject=subject, msg=massage, imageErr=imageErr)

        sbj = 'گزارش خطا'
        from_email = settings.EMAIL_HOST_USER
        to = 'peakabot@gmail.com'
        html_content = f'<div style="border: 1px dashed gray; border-radius: 10px;padding: 20px; margin: 10px 50px; direction: rtl; background: linear-gradient(rgb(203, 203, 248),white, rgb(203, 203, 248));"><h3 style="color: red;">گزارش خطا</h3><p> ایمیل: {email}	<br>عنوان خطا: {subject}<br>متن خطا: {massage}<br></p></div>'
        msg = EmailMessage(sbj, html_content, from_email, [to])
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()
        messages.info(request, 'گزارش خطای شما با موفقیت انجام شد. در اسرع وقت رسیدگی میشود. ممنون از تبادلاتی که با وبسایت دارید.')
        return redirect('/')

    return render(request, 'report_spam.html', context)

def sendEmail_forgetPw(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.POST:
        emailForget = request.POST.get('emailForget')
        if emailForget:
            user = User.objects.filter(email__iexact=emailForget).first()
            if user:
                # send Mail
                subject = 'ارسال لینک برای بازیابی رمز عبور'
                from_email = settings.EMAIL_HOST_USER
                to = user.email

                html_content = f'<div style="border: 1px dashed gray; border-radius: 10px;padding: 20px; margin: 10px 50px; direction: rtl; background: linear-gradient(rgb(203, 203, 248),white, rgb(203, 203, 248));"><h3 style="color: red;">بازیابی رمز عبور</h3><p>با عرض سلام و درود،<br>ایمیل شما با موفقیت تایید شد، شما میتوانید از لینک زیر رمزعبور خود را تغییر دهید.	<br><br><a href="http://127.0.0.1:8000/Auth/forget/email/send/changepage?email={user.email}" style="color:blue; text-decoration:none;">بازیابی رمز عبور</a></p></div>'
                msg = EmailMessage(subject, html_content, from_email, [to])
                msg.content_subtype = "html"  # Main content is now text/html
                msg.send()
                messages.info(request, 'ایمیلی برای شما ارسال گردید.')

            else:
                messages.info(request, 'ایمیلی با این آدرس وجود ندارد.')

    return render(request, 'email-forget-pw-1.html', {})

def change_forgetPw(request):
    if request.user.is_authenticated:
        return redirect('/')

    email = request.GET.get('email')
    user: User = User.objects.filter(email__iexact=email).first()
    if user:
        pw1 = request.POST.get('pw1')
        pw2 = request.POST.get('pw2')
        if pw1 and pw2 and pw1 != '':
            if pw2 == pw1:
                user.set_password(pw2)
                user.save()
                messages.info(request, 'رمز عبور با موفقیت تغییر کرد!')
                return redirect('/Auth/Login')
            else:
                messages.info(request, 'دو رمز عبور باید یکسان باشند.')
        else:
            messages.info(request,'دو فیلد را پر کنید!!')
    else:
        messages.info(request, 'کاربری با این ایمیل وجود ندارد.')
        return redirect('/')

    return render(request, 'forget-pw-2.html', {})