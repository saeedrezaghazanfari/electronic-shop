from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import EditForm, ChangePw
from Eshop_Auth.models import UltraProfile
from django.contrib import messages
from Eshop_Other.models import Send_Notifications_email_Model, Emails
from Eshop_Product.models import Favorites, Product
from Eshop_Order.models import Order, OrderDetails
from django.conf import settings
from django.core.mail import EmailMessage, send_mail

@login_required(login_url='/Auth/Login')
def pannel_Page(request):
    userid = request.user.id
    user = User.objects.get(id=userid)

    userProfile = UltraProfile.objects.filter(user_id=userid).first()

    favs = Favorites.objects.filter(user_id=request.user.id).all()

    context = {'user':user,'userProfile':userProfile, 'favs':favs}
    return render(request, 'pannelhome.html', context)

@login_required(login_url='/Auth/Login')
def returnShowProd(request, *args, **kwargs):
    productID = kwargs.get('productID')
    prod = Product.objects.get(id=productID)
    return redirect(f'/Product/Details/{productID}/{prod.title.replace(" ","-")}')

@login_required(login_url='/Auth/Login')
def rmeovefavoritesUser(request, *args, **kwargs):
    productID = kwargs.get('productID')
    Favorites.objects.filter(user_id=request.user.id, product_id=productID).delete()
    messages.info(request, 'محصول با موفقیت حذف شد!')
    return redirect('/user/info')

@login_required(login_url='/Auth/Login')
def edit_Page(request):
    userid = request.user.id
    myuser: User = User.objects.get(id=userid)
    userProfile = UltraProfile.objects.filter(user_id=userid).first()

    if not UltraProfile.objects.filter(user_id=myuser.id).first():
        myuser.ultraprofile_set.create(avator=UltraProfile.set_image_profile(), phone=0, webName='', bio=' ')

    editform = EditForm(request.POST or None, initial={
        'firstname': request.user.first_name,
        'lastname':request.user.last_name,
        'bio':userProfile.bio,
        'phone': userProfile.phone,
        'webName': userProfile.webName
    })

    userObj: User = User.objects.filter(id=userid).first()
    userProfile: UltraProfile = UltraProfile.objects.filter(user_id=userid).first()

    context = {
        'editform': editform,
        'userProfile': userProfile
    }

    if editform.is_valid():

        firstname = editform.cleaned_data.get('firstname')
        lastname = editform.cleaned_data.get('lastname')
        phone = editform.cleaned_data.get('phone')
        bio = editform.cleaned_data.get('bio')
        webName = editform.cleaned_data.get('webName')

        userObj.first_name = firstname
        userObj.last_name = lastname
        userObj.save()

        userProfile.phone = phone
        userProfile.bio = bio
        userProfile.webName = webName
        userProfile.save()

        messages.info(request, 'پروفایل شما با موفقیت ویرایش شد.')
        return redirect('/user/info')

    return render(request, 'editpannel.html', context)

@login_required(login_url='/Auth/Login')
def sideBar(request):
    userid = request.user.id
    userProfile = UltraProfile.objects.filter(user_id=userid).first()

    return render(request, 'sidebar.html', {'userProfile':userProfile})

def ProfileImagesideBar(request):
    userid = request.user.id
    userProfile = UltraProfile.objects.filter(user_id=userid).first()

    try:
        if request.POST:
            avatorImage = request.FILES['avatorImage']
            if avatorImage:
                userProfile.avator = avatorImage
                userProfile.save()
                messages.info(request, 'تصویر پروفایل شما با موفقیت ثبت شد.')
    except:
        pass

    return render(request, 'imageprofile_partial.html', {'userProfile':userProfile})

@login_required(login_url='/Auth/Login')
def ChangePW_page(request):
    userid = request.user.id
    user: User = User.objects.get(id=userid)
    # changePw = ChangePw(request.POST or None)
    # context = {'changePw': changePw}

    if request.POST:
        pass1 = request.POST.get('newPass1')
        pass2 = request.POST.get('newPass2')
        if pass1 == pass2 and pass1 != '':
            user.set_password(pass1)
            user.save()
            messages.info(request, 'تغییر رمز با موفقیت انجام شد!! برای ورود دوباره ، اطلاعات حساب خود را وارد کنید.')
            return redirect('/user/info')
        else:
            messages.info(request, 'تغییر رمز با مشکل روبرو شد، دوباره امتحان کنید!!')
            return redirect('/user/change-pw')

    # if changePw.is_valid():
    #     old_password = changePw.cleaned_data.get('old_password')
    #     new_pw_1 = changePw.cleaned_data.get('new_pw_1')
    #     new_pw_2 = changePw.cleaned_data.get('new_pw_2')
    #     if user.password != old_password:
    #         return changePw.add_error('old_password', 'رمز قدیمی مطابقت ندارد!!')
    #     elif user.password == old_password:
    #         user.set_password(new_pw_2)
    #         user.save()
    #         messages.info(request, 'تغییر رمز با موفقیت انجام شد!!')
    #         return redirect('/user/info')

    return render(request, 'change_pw.html', {})

@login_required(login_url='/Auth/Login')
def factors_page(request):
    myorder: Order = Order.objects.get(owner_id=request.user.id)
    orders = myorder.orderdetails_set.all().order_by('-id')
    ex = False
    if orders:
        ex = True
    context = {
        'myorder': myorder,
        'orders': orders,
        'ex': ex
    }
    return render(request, 'factors.html', context)

@login_required(login_url='/Auth/Login')
def notifications_Page(request):
    thisUser = request.user
    context = {
        'activess': None
    }
    if not Send_Notifications_email_Model.objects.filter(user_id=thisUser.id).first():
        Send_Notifications_email_Model.objects.create(user_id=thisUser.id, activeSend=True)

    if request.POST:
        sendMail = request.POST.get('sendMail')
        if sendMail == 'yesSending':
            if Send_Notifications_email_Model.objects.filter(user_id=thisUser.id).first():
                sendmailer = Send_Notifications_email_Model.objects.filter(user_id=thisUser.id).first()
                sendmailer.activeSend = True
                sendmailer.save()
                messages.info(request, 'تغییر با موفقیت ثبت شد.')
                return redirect('/user/info')

        elif sendMail == 'noSending':
            if Send_Notifications_email_Model.objects.filter(user_id=thisUser.id).first():
                sendmailer = Send_Notifications_email_Model.objects.filter(user_id=thisUser.id).first()
                sendmailer.activeSend = False
                sendmailer.save()
                messages.info(request, 'تغییر با موفقیت ثبت شد.')
                return redirect('/user/info')

    user = Send_Notifications_email_Model.objects.filter(user_id=thisUser.id).first()
    if user:
        context['activess'] = user.activeSend
    return render(request, 'notifications.html', context)

@login_required(login_url='/Auth/Login')
def adminSendMails(request):
    if not request.user.is_superuser:
        return redirect('/')

    thisUser = request.user
    emailContent: Emails = Emails.objects.last()
    ex = False
    if emailContent:
        ex = True
    activeusers: Send_Notifications_email_Model = Send_Notifications_email_Model.objects.filter(activeSend=True).all()
    if activeusers:
        activemails = []
        for i in activeusers:
            activemails.append(i.user.email)
    else:
        messages.info(request, 'ایمیلی برای ارسال وجود ندارد.')

    if request.method == 'POST':
        if request.POST.get('switchMail') == 'send':
            subject = emailContent.subject
            from_email = settings.EMAIL_HOST_USER
            to = activemails
            html_content = emailContent.content

            msg = EmailMessage(subject, html_content, from_email, to)
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send()

            messages.info(request, 'ایمیل ها با موفقیت ارسال شدند!!')
        else:
            messages.info(request, 'هیچ ایمیلی ارسال نشد!')

    context = {
        'emailCntent':emailContent,
        'ex':ex
    }
    return render(request, 'adminsendmails.html', context)

@login_required(login_url='/Auth/Login')
def adminOption_users(request):
    if not request.user.is_superuser:
        return redirect('/')

    # Get Online Users
    from online_users.models import OnlineUserActivity
    from datetime import timedelta
    user_activity_objects = OnlineUserActivity.get_user_activities(timedelta(minutes=15))
    activeUsersNUM = user_activity_objects.count()
    activeUsersID = OnlineUserActivity.objects.values_list('user_id', flat=True)
    activeUsersNAMES = []
    for i in activeUsersID:
        activeUsersNAMES.append(User.objects.get(id=i))

    users = User.objects.all().order_by('-id')
    context = {
        'users':users,
        'IP': request.META.get('REMOTE_ADDR'),
        'activeUsers':activeUsersNUM,
        'activeUsersID':activeUsersID,
        'activeUsersNAMES':activeUsersNAMES
    }
    return render(request, 'adminusers.html', context)

@login_required(login_url='/Auth/Login')
def adminOption_users_Action(request, *args, **kwargs):
    if not request.user.is_superuser:
        return redirect('/')

    userID = kwargs.get('userID')

    if request.POST:
        adminstatus = request.POST.get('adminstatus')
        removeUser = request.POST.get('removeUser')
        activeUser = request.POST.get('activeUser')

        if adminstatus == 'yes':
            user = User.objects.get(id=userID)
            user.is_superuser = True
            user.save()

        elif adminstatus == 'no':
            user = User.objects.get(id=userID)
            user.is_superuser = False
            user.save()

        if activeUser == 'yes':
            user = User.objects.get(id=userID)
            user.is_active = True
            user.save()

        elif activeUser == 'no':
            user = User.objects.get(id=userID)
            user.is_active = False
            user.save()

        if removeUser == 'yes':
            user = User.objects.get(id=userID).delete()
    messages.info(request, 'تغییرات با موفقیت اعمال شد!!')
    return redirect('/user/admin/users')

@login_required(login_url='/Auth/Login')
def charts_Page(request):
    if not request.user.is_superuser:
        return redirect('/')
    return render(request, 'charts.html', {})

@login_required(login_url='/Auth/Login')
def deleteUser(request):
    thisUserID = request.user.id
    if request.POST:
        if request.POST.get('switchdel') == 'del':
            User.objects.get(id=thisUserID).delete()
            messages.info(request, 'حساب کاربری شما با موفقیت حذف شد. برای ایجاد حساب کاربری اطلاعات خود را وارد کنید.')
            return redirect('/Auth/Register')
        else:
            messages.info(request, 'حذف حساب کاربری شما انجام نشد.')

    return render(request, 'deleteuser.html', {})