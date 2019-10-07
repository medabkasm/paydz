from django.urls import path , include,re_path , reverse
from django.contrib.auth import views as auth_views
from .views import *

app_name = 'profiles'

urlpatterns = [
    path('<str:username>/',profile_view,name = 'profile'),
    path('<username>/password_set/',password_set_view , name = 'password_set'),
    path('<str:username>/password_change/',
            auth_views.PasswordChangeView.as_view(template_name = "profiles/changePassword.html",
                success_url ='done/'),
                                name='password_change'),

    path('<str:username>/password_change/done/',
            auth_views.PasswordChangeDoneView.as_view(template_name = "profiles/changePasswordDone.html") ,
                                                name='password_change_done'),
    path('<username>/delete/',profile_delete_view_ajax,name = 'profile_delete_ajax'),
    path('<username>/edit/',profile_edit_view_ajax,name = 'profile_edit_ajax'),
    path('<username>/data/<data>/',profile_view_ajax , name = 'profile_data_ajax'),



]
