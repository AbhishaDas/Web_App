import email
from typing import Required
from django.db import models

# Create your models here.
class userinfo(models.Model):
    firstname=models.CharField(max_length=200)
    lastname=models.CharField(max_length=200)
    email=models.EmailField(Required=True)
    username=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    
    
    def __str__(self):
        return self.username