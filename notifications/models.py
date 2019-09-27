from django.db import models
from	django.utils.translation	import	gettext_lazy	as	_
from accounts.models import *
from offers.models import *
# Create your models here.






CONTENT = (
    ("Bug",_("Bug")),
    ("Partenership",_("Partenership")),
    ("Donate",_("Donate")),
    ("Other",_("Other")),
)

class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.CharField(choices = CONTENT , max_length = 20)
    date = models.DateTimeField(auto_now_add = True)
    contactMessage = models.CharField(max_length = 400)

    def __str__(self):
        return 'message from : ' + self.user.username


TYPE = (
    ('notification',_('notification')),
    ('message',_('message')),
)

class Notification(models.Model):
    notif = models.OneToOneField(Offer,on_delete = models.CASCADE , null = True , blank = True)
    msg = models.OneToOneField(Message,on_delete = models.CASCADE , null = True , blank = True)
    date = models.DateTimeField(auto_now_add = True)
    type = models.CharField(choices = TYPE , max_length = 20)
    seen = models.BooleanField(default = False)

    def __str__(self):
        return 'notification : ' + self.type
