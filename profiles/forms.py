
from django import forms
from accounts.models import *
from	django.utils.translation	import	gettext_lazy	as	_




class profileEditForm(forms.ModelForm):     # form for creating / editing  a profile
    class Meta:
        model = Profile
        fields = ('firstName','lastName','gender','birthday','wilaya','pofileUsage',)

class userEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','phone','email')
