from django.urls import path

from .views import Login_Page, Logout_Page, Register_Page, report_spam, sendEmail_forgetPw, change_forgetPw, pre_home_page

urlpatterns = [
    path('Auth/Login', Login_Page),
    path('Auth/pre-home', pre_home_page),
    path('Auth/Logout', Logout_Page),
    path('Auth/Register', Register_Page),
    path('report-Spam', report_spam),
    path('Auth/send-email-pw', sendEmail_forgetPw),
    path('Auth/forget/email/send/changepage', change_forgetPw),
]