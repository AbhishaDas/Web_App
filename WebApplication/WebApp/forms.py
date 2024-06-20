#forms.py
from django import forms
from django.forms import ModelForm
from .models import userinfo

class UserForm(ModelForm):
    class Meta:
        model = userinfo
        fields = '__all__'