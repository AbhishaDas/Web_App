#forms.py
from django import forms
from django.forms import ModelForm
from .models import UserInfo

class UserForm(ModelForm):
    class Meta:
        model = UserInfo
        fields = '__all__'
        exclude = ['username', 'password']