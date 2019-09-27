"""paysera URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from django.contrib.auth import views as auth_views
from django.conf.urls.i18n import i18n_patterns
from .views import *
from profiles.views import *

urlpatterns = [
    path('offers/',include('offers.urls',namespace = 'offers')),
    path('notification/',include('notifications.urls',namespace = 'notifications')),
    path('profiles/<username>/delete/',profile_delete_view_ajax,name = 'profile_delete_ajax'),
    path('profiles/<username>/edit/',profile_edit_view_ajax,name = 'profile_edit_ajax'),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('dash_board/<str:notification>/<str:action>/<int:pk>/',dash_board_ajax),
    path('dash_board/',dash_board_view , name = "dash_board"),
    path('',include('home.urls',namespace = 'home')),
    path('accounts/',include('accounts.urls' , namespace = 'accounts')),
    path('profiles/',include('profiles.urls',namespace = 'profiles')),
    path('oauth/', include('social_django.urls', namespace = 'social')),
)
