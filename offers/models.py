from django.db import models
from	django.utils.translation	import	gettext_lazy	as	_
from django.core.validators import MinValueValidator
from accounts.validators import *
from accounts.models import *
# Create your models here.


ACTIVITE = (
    ('buy',_('BUY')),
    ('sell',_('SELL')),
)
CURRENCY = (
    ('EUR','EUR'),
    ('USD','USD'),
)
class Offer(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    date = models.DateTimeField(auto_now_add = True)
    activitiy = models.CharField(choices = ACTIVITE, null=True) # 5
    price = models.FloatField(validators = [positive_number_validation,])
    amount = models.FloatField(validators = [positive_number_validation,])
    cost = models.FloatField(validators = [positive_number_validation,], null=True)
    currency = models.CharField(choices = CURRENCY , max_length = 4)
    message = models.CharField(blank = True , default = "empty",null = True) # 255
    def __str__(self):
        return self.user.username +"'s offer" + str(self.pk)
