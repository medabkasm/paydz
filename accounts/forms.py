# accounts.forms.py
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.template.defaultfilters import slugify
from django.utils import timezone
from .models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as	_


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField()
    password2 = forms.CharField(label='Confirm password')

    class Meta:
        model = User
        fields = ('email','username','phone')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError(_("email is taken"))
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        qs = User.objects.filter(phone = phone)
        if qs.exists():
            raise forms.ValidationError(_("phone number already in use"))
        return phone

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username = username)
        if qs.exists():
            raise forms.ValidationError(_("username exists"))
        return username

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        condition1 = ( password1 and password2 )
        condition2 = ( password1 == password2 )
        condition3 = ( len(password2) > 8 )
        if not ( condition1 and condition2 ):
            raise forms.ValidationError(_("Passwords don't match"))
        if not condition3:
            raise forms.ValidationError(_("Password length less than 8"))

        return password2
