from django import forms
from django.forms import ModelForm
from .models import movie_info, userinfo

class UserForm(ModelForm):
    class Meta:
        model =userinfo
        fields ='__all__'   