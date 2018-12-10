from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password
# Create your models here.

class Users(models.Model):
    name=models.CharField(max_length=25)
    #password=models.BigIntegerField(default=hash(123456))
    password=models.CharField(max_length=200,default=make_password('123456'))
    last_login_time=models.DateTimeField('last login time',default=timezone.now)
    def __str__(self):
        return self.name
