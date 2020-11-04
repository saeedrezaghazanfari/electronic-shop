from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Eshop_Order.models import Order, OrderDetails, OffCode
from Eshop_Product.models import Product
from .forms import OrderForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from django.http import HttpResponse
from zeep import Client
import time

@login_required(login_url='/Auth/Login')
def order_page(request):
    ex = False
    orderUser: Order = Order.objects.filter(owner_id=request.user.id, is_paid=False).first()
    userOrder = 0

    if orderUser:
        orders = orderUser.orderdetails_set.all()
        if orders:
            ex = True
        else:
            ex = False
        userOrder = orderUser.get_final_total()

    elif orderUser is None:
        orders = False
        ex = False

    context = {
        'ex': ex,
        'orders': orders,
        'userOrder': userOrder
    }
    return render(request, 'open_order.html', context)

@csrf_exempt
def order_page_ajax(request):
    if request.is_ajax():
        CopenCode = request.POST.get('a')
        ex = OffCode.objects.filter(offcode__exact=CopenCode, active=True).first()
        if ex:
            codeMany = ex.many
            percentOff = codeMany / 100

            order: Order = Order.objects.filter(owner_id=request.user.id, is_paid=False).first()
            filnailTotal = order.get_final_total()

            final_total_off = filnailTotal * percentOff
            return JsonResponse({'valid': True, 'final_total_off': final_total_off})
        return JsonResponse({'valid': False})

@login_required(login_url='/Auth/Login')
def add_user_order(request):
    thisUser = request.user
    orderForm = OrderForm(request.POST or None)

    if orderForm.is_valid():

        if request.POST:
            selectColor = request.POST.get('selectColor')
        productId = orderForm.cleaned_data.get('productId')
        count = orderForm.cleaned_data.get('count')

        order: Order = Order.objects.filter(owner_id=thisUser.id, is_paid=False).first()
        if not order:
            order: Order = Order.objects.create(owner_id=thisUser.id, is_paid=False)

        if not order.orderdetails_set.filter(product_id=productId,).first():
            if count <= 0:
                count = 1
            productselected: Product = Product.objects.get(id=productId)
            order.orderdetails_set.create(product_id=productId, count=count, price=productselected.price, productColor=selectColor)
            messages.info(request, 'محصول با موفقیت به سبد خرید اضافه شد!')
            return redirect('/my-order')
        else:
            messages.info(request, 'این محصول در سبد خرید موجود میباشد!!')
            return redirect('/my-order')

    return redirect('/my-order')

# ZarinPal Code

# MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
# client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
# # amount = 1000  # Toman / Required
# description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
# email = 'saeedreza.gh.1397@gmail.com'  # Optional
# mobile = '09037279147'  # Optional
# CallbackURL = 'http://localhost:8000/verify' # Important: need to edit for realy server.
#
# @login_required(login_url='/Auth/Login')
# def send_request(request):
#     totalPrice = 0
#     order = Order.objects.filter(owner_id=request.user.id, is_paid=False).first()
#     if order:
#         ex = OffCode.objects.filter(offcode__exact=CopenCode, active=True).first()
#         if ex:
#             codeMany = ex.many
#             percentOff = codeMany / 100
#             filnailTotal = order.get_final_total()
#             totalPrice = filnailTotal * percentOff
#
#         result = client.service.PaymentRequest(MERCHANT, totalPrice, description, email, mobile, f'{CallbackURL}/{order.id}')
#         if result.Status == 100:
#             return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
#         else:
#             return HttpResponse('Error code: ' + str(result.Status))
#
# @login_required(login_url='/Auth/Login')
# def verify(request, *args, **kwargs):
#     OrderID = kwargs.get('OrderID')
#     thisUser = request.user
#
#     if request.GET.get('Status') == 'OK':
#         result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
#         if result.Status == 100:
#             myOrder = Order.objects.get(id=OrderID)
#             myOrder.is_paid = True
#             myOrder.paymentDate = time.time()
#             myOrder.ref_Id = myOrder.get_ref_id()
#             myOrder.save()
#             # return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
#             messages.info(request, f'پرداخت شما با موفقیت انجام شد! <br/> کد پیگیری: {myOrder.ref_Id}')
#             return redirect('/')
#         elif result.Status == 101:
#             return HttpResponse('تراکنش درحل انجام است : ' + str(result.Status))
#         else:
#             return HttpResponse('تراکنش نا موفق بود.\nوضعیت: ' + str(result.Status))
#     else:
#         return HttpResponse('عملیات تراکنش به وسیله ی شما لغو شد!!')



def plusOrder(request, *args, **kwargs):
    OrderId = kwargs.get('OrderId')
    orderd = OrderDetails.objects.get(id=OrderId)
    orderd.count = orderd.count + 1
    orderd.save()
    return redirect('/my-order')

def minesOrder(request, *args, **kwargs):
    OrderId = kwargs.get('OrderId')
    if OrderDetails.objects.get(id=OrderId).count <= 1:
        return redirect('/my-order')
    orderd = OrderDetails.objects.get(id=OrderId)
    orderd.count = orderd.count - 1
    orderd.save()
    return redirect('/my-order')

def removeOrder(request, *args, **kwargs):
    OrderId = kwargs.get('OrderId')
    OrderDetails.objects.get(id=OrderId).delete()
    messages.info(request, f'کالا با موفقیت از سبد خرید حذف شد!!')
    return redirect('/my-order')
