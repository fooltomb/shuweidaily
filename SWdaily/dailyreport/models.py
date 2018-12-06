from django.db import models

# Create your models here.
class Users(models.Model):
    userid=models.IntegerField(default=0)
    name=models.CharField(max_length=25)
    def __str__(self):
        return self.name
