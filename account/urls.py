from django.urls import path
from knox import views as knox_views
from django.contrib.auth.views import LogoutView
from django.conf.urls import url
from account.views import (register_page, phone_validation,
                           otp_validator, login_page, set_password,
                           registeration, LoginView, passwordrecovery_page,
                           change_password, phone_validation_passchange,
                           new_password_replace, dashboard_page,
                           userinfo, edituserinfo, addnewlocation,
                           userlocation, getuserlike, getuserbookmark, getcummentuser)


urlpatterns = [
    path('user-cumment/', getcummentuser, name='getcummentuser'),
    path('user-bookmark/', getuserbookmark, name='getuserbookmark'),
    path('user-likes/', getuserlike, name='getuserlike'),
    path('locations/', userlocation, name='userlocation'),
    path('addlocation/', addnewlocation, name='addnewlocation'),
    path('edit/', edituserinfo, name='edituserinfo'),
    path('userinformations/', userinfo, name='userinfo'),
    path('dashboard/', dashboard_page, name='dashboard_page'),
    path('new_password_replace/', new_password_replace, name='new_password_replace'),
    path('phone_validation_pass/', phone_validation_passchange, name='phone_validation_passchange'),
    path('password_change/', change_password, name='change_password'),
    path('password-recovery/', passwordrecovery_page, name='passwordrecovery_page'),
    path('registration/', register_page, name='register_page'),
    path('user_registeration/', registeration, name='registeration'),
    path('password/', set_password, name='set_password'),
    path('loginuser/', login_page, name='login_page'),
    path('validation_number/', phone_validation, name='phone_validation'),
    path('validation_otp/', otp_validator, name='otp_validator'),
    url(r'login/', LoginView.as_view(), name='knox_login'),
    url(r'logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logout_user/', LogoutView.as_view(), name='logout'),
]
