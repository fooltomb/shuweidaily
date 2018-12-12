from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password
# Create your models here.

class Users(models.Model):
    name=models.CharField(max_length=25)
    #password=models.BigIntegerField(default=hash(123456))
    password=models.CharField(max_length=200,default=make_password('123456'))
    superuser=models.BooleanField(default=False)
    last_login_time=models.DateTimeField('last login time',default=timezone.now)
    def __str__(self):
        return self.name

class Project(models.Model):
    name=models.CharField(max_length=45)
    detail=models.TextField(max_length=255)
    start_date=models.DateField(default=timezone.now)
    end_date=models.DateField()
    isWorking=models.BooleanField(default=True)
    reward=models.IntegerField()
    def __str__(self):
        return self.name


class Report(models.Model):
    author=models.ForeignKey(Users,on_delete=models.CASCADE)
    pub_date=models.DateField()
    def __str__(self):
        return str(self.pub_date)

class ReportToProject(models.Model):
    report=models.ForeignKey(Report,on_delete=models.CASCADE,default=None)
    project=models.ForeignKey(Project,on_delete=models.CASCADE,default=None)
    weight=models.FloatField(default=0.0)
    def __str__(self):
        return self.id
