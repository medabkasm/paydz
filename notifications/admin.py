from django.contrib import admin
from .models import Notification
# Register your models here.
class NotificationsAdminManager(admin.ModelAdmin):
    class Meta:
        model = Notification

admin.site.register(Notification ,NotificationsAdminManager)
