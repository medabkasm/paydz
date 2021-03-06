from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
from django import forms
from django.dispatch import receiver
from django.urls import reverse
from .validators import *
from	django.utils.translation	import	gettext_lazy	as	_
# Create your models here.


class User(AbstractUser):
    email = models.EmailField(max_length = 255,unique = True , validators = [fake_email_validation,] )
    username = models.CharField(max_length = 20,unique = True )
    phone = models.CharField(max_length = 10 ,unique = True ,default = "xxxxxxxxx" ,validators = [phone_number_validation,])
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
    firstName = models.CharField( _('first name'),max_length = 20, blank = True , null = True)
    lastName = models.CharField(_('last name'),max_length = 20,  blank = True , null = True)
    gender = models.CharField(_('gender') , choices = GENDER ,max_length = 10 , blank = True , null = True)
    profileImage = models.ImageField(_('profile image'),upload_to = 'usersImages' , blank = True,null=True)
    coverImage = models.ImageField(_('cover image'),upload_to = 'usersImages' , blank = True,null=True)
    #birthday = models.DateField(_('birthday'),blank = True , null = True )
    age = models.IntegerField(_('age'),blank = True , default = 18 ,null = True)

    address = models.CharField(_('addess'),max_length = 100 ,  blank = True , null = True)
    pofileUsage = models.CharField(_('profile usage'),choices = USAGE ,max_length = 15 ,  blank = True , null = True)
    profileComplete = models.BooleanField(default ='False')

    def __str__(self):  # string representation of the profile when it get created.
        return slugify(self.user.username + '__Profile')
