from django.contrib import admin
from django.urls import path , include

from .views import *

app_name = 'home'
urlpatterns = [
    path('',Index.as_view(),name = 'posts'),
    #path('home/post/<int:id>/',postDetails.as_view(),name = 'post')
    
]
