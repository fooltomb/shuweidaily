from django.db import models
from django.utils import timezone
# Create your models here.
class Users(models.Model):
    userid=models.IntegerField(default=0)
    name=models.CharField(max_length=25)
    password=models.BigIntegerField(default=hash(123456))
    last_login_time=models.DateTimeField('last login time',default=timezone.now)
    def __str__(self):
        return self.name
