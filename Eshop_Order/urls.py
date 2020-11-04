from django.urls import path

from Eshop_Order.views import (
    # send_request,
    # verify,
    order_page,
    order_page_ajax,
    add_user_order,
    plusOrder,
    minesOrder,
    removeOrder,
)

urlpatterns = [
    # path('send-request/', send_request),
    # path('verify/<int:OrderID>', verify),

    path('my-order', order_page),
    path('my-order-ajax', order_page_ajax, name="openOffCode"),
    path('add-user-order', add_user_order),
    path('add-one-to-product/<int:OrderId>', plusOrder),
    path('mines-one-from-product/<int:OrderId>', minesOrder),
    path('remove-from-product/<int:OrderId>', removeOrder),
]