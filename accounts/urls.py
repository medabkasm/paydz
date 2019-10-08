from django.contrib import admin
from django.urls import path , include , reverse_lazy , re_path
from .views import *
from django.contrib.auth import views as auth_views


app_name = 'accounts'
urlpatterns = [
    #path('register/activate/<uidb64>/<token>/',user_activation_view , name = 'activate'),
    re_path(r'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[.]*)/$', user_activation_view , name = 'activate'),
    path('register/',RegisterView.as_view(),name = 'register'),
    path('login/',auth_views.LoginView.as_view(template_name = 'accounts/registration/login.html' , redirect_authenticated_user = True),name = 'login'),
    path('logout/',auth_views.LogoutView.as_view(template_name = 'accounts/registration/logged_out.html'),name = 'logout'),
    path('password_reset/',auth_views.PasswordResetView.as_view(
                                            template_name ='accounts/registration/password_reset.html',
                                            email_template_name = 'accounts/registration/password_reset_email.html',
                                            success_url='done/'),
                            name='password_reset'),

    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(
                                            template_name ='accounts/registration/password_reset_done.html'),
                            name='password_reset_done'),

    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(
                                            template_name ='accounts/registration/password_reset_confirm.html',
                                            success_url ='done/'),
                            name='password_reset_confirm'),

    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(
                                            template_name ='accounts/registration/password_reset_complete.html'),
                            name='password_reset_complete'),


]
