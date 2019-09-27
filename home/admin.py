from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Post)  # add the Profile model to the admin panel.
admin.site.register(HashTag)
