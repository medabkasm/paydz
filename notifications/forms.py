from .models import Message
from django import forms

class messageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('content','contactMessage')
