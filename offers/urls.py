from django.contrib import admin
from django.urls import path , include
from .views import *

app_name = 'offers'
urlpatterns = [
    path('<offer>/',offer_view , name = 'offer'),
]
