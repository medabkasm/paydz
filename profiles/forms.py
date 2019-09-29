
from django import forms
from accounts.models import *
from	django.utils.translation	import	gettext_lazy	as	_
from bootstrap_datepicker_plus import DatePickerInput
from django import forms


class profileEditForm(forms.ModelForm):     # form for creating / editing  a profile
    class Meta:
        model = Profile
        fields = ('firstName','lastName','gender','age','address','pofileUsage',)


class userEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','phone','email')




def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)
