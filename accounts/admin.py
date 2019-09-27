from django.contrib import admin
from .models import *  # User , Profile
from .forms import *   # UserAdminCreationForm , UserAdminChangeForm
# Register your models here.

class UserAdminManager(admin.ModelAdmin):
    search_fields = ['email','username','phone']
    class Meta:
        model = User

class UserRegister(admin.ModelAdmin):
    class Meta:
        model = User
class ProfileAdminManager(admin.ModelAdmin):
    search_fields = ['firstName','lastName',]
    class Meta:
        model = Profile
admin.site.register(User , UserAdminManager)  # add the user model to the admin pagnel.
admin.site.register(Profile , ProfileAdminManager)
