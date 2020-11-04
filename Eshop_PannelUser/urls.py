from django.urls import path

from Eshop_PannelUser.views import (

    pannel_Page,
    rmeovefavoritesUser,
    adminSendMails,
    edit_Page,
    sideBar,
    ChangePW_page,
    factors_page,
    notifications_Page,
    adminOption_users,
    adminOption_users_Action,
    returnShowProd,
    ProfileImagesideBar,
    charts_Page,
)

urlpatterns = [
    path('info', pannel_Page),
    path('fav', pannel_Page),
    path('favorites/show/<int:productID>', returnShowProd),
    path('favorites/remove/<int:productID>', rmeovefavoritesUser),
    path('edit', edit_Page),
    path('admin/charts', charts_Page),
    path('change-pw', ChangePW_page),
    path('my-factors', factors_page),
    path('notifications', notifications_Page),
    path('admin/users', adminOption_users),
    path('admin/users/<int:userID>', adminOption_users_Action),
    path('admin/send-mails', adminSendMails),
    path('sideBar', sideBar),
    path('Profile-Image-sideBar', ProfileImagesideBar, name='ProfileImagesideBar'),

]