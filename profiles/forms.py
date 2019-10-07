
from django import forms
from accounts.models import *
from	django.utils.translation	import	gettext_lazy	as	_
from django import forms
from accounts.validators import *

class profileEditForm(forms.ModelForm):     # form for creating / editing  a profile
    class Meta:
        model = Profile
        fields = ('firstName','lastName','gender','age','address','pofileUsage',)


class userEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','phone','email')


class PhoneForm(forms.Form):
    phone = forms.CharField(max_length = 10  ,validators = [phone_number_validation,])

def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)
