from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from .validators import *
from	django.utils.translation	import	gettext_lazy	as	_
# Create your models here.


class User(AbstractUser):
    email = models.EmailField(max_length = 255,unique = True , validators = [fake_email_validation,] )
    username = models.CharField(max_length = 20 , unique = True )
    phone = models.CharField(unique = True , max_length = 10 ,validators = [phone_number_validation,])
    joined = models.DateTimeField(auto_now_add = True)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    is_admin = models.BooleanField(default = False)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username','phone']

    def __str__(self):
        return self.username


USAGE = (
    ('BUY',_('BUY')),
    ('SELL',_('SELL')),
    ('BOTH',_('BOTH')),
)
GENDER = (
    ('MALE',_('MALE')),
    ('FEMALE',_('FEMALE')),
)

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE,unique = True)
    firstName = models.CharField( _('first name'),max_length = 20, default = _("First Name"))
    lastName = models.CharField(_('last name'),max_length = 20, default = _("Last Name"))
    gender = models.CharField(_('gender') , choices = GENDER ,max_length = 10 ,default = _("Gender"))
    profileImage = models.ImageField(_('profile image'),upload_to = 'usersImages' , blank = True,null=True)
    coverImage = models.ImageField(_('cover image'),upload_to = 'usersImages' , blank = True,null=True)
    birthday = models.DateField(_('birthday'),blank = True , null = True )
    wilaya = models.CharField(_('wilaya'),max_length = 30 ,blank = True ,null = True , default = _("wilaya"))
    pofileUsage = models.CharField(_('profile usage'),choices = USAGE ,max_length = 15 , default = _("Profile Usage"))
    profileComplete = models.BooleanField(default ='False')

    def __str__(self):  # string representation of the profile when it get created.
        return slugify(self.user.username + '__Profile')
