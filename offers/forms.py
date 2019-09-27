from django import forms
from .models import *



class offerForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ('price','amount','currency','message')
