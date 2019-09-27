from django.urls import path , include
from .views import *

app_name = 'notifications'
urlpatterns = [
    path('message/',message_view , name = 'message'),
    path('details/<pk>/',notification_view , name = 'notificationDetails'),

]
