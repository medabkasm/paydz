from django.contrib import admin
from .models import *

# Register your models here.

class OffersAdminManager(admin.ModelAdmin):
    search_fields = ['user','date','activitiy']
    class Meta:
        model = Offer

admin.site.register(Offer ,OffersAdminManager)
