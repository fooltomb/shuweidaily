# -*- coding:utf-8 -*-
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password
# Create your models here.

class Users(models.Model):
    name=models.CharField(max_length=25)
    password=models.CharField(max_length=200,default=make_password('123456'))
    superuser=models.BooleanField(default=False)
    active=models.BooleanField(default=True)
    last_login_time=models.DateTimeField('last login time',default=timezone.now)
    join_date=models.DateField(default=timezone.now)
    leave_date=models.DateField(default=timezone.now)
    def __str__(self):
        return self.name

class Project(models.Model):
    name=models.CharField(max_length=45)
    detail=models.TextField(max_length=255)
    start_date=models.DateField(default=timezone.now)
    end_date=models.DateField(default=timezone.now)
    isWorking=models.BooleanField(default=True)
    spend_weight=models.FloatField(default=0.0)
    reward=models.IntegerField(default=0)
    def addWeight(self,w):
        self.spend_weight+=w
    def __str__(self):
        return self.name


class Report(models.Model):
    author=models.ForeignKey(Users,on_delete=models.CASCADE)

    pub_date=models.DateField()
    project1=models.CharField(max_length=45,default="无/学习")
    weight1=models.FloatField(default=0.0)
    project2=models.CharField(max_length=45,default="无/学习")
    weight2=models.FloatField(default=0.0)
    project3=models.CharField(max_length=45,default="无/学习")
    weight3=models.FloatField(default=0.0)
    detail=models.TextField(max_length=140)
    def __str__(self):
        return str(self.author)+str(self.pub_date)

class UserToProject(models.Model):
    author=models.ForeignKey(Users,on_delete=models.CASCADE,default=None)
    project=models.ForeignKey(Project,on_delete=models.CASCADE,default=None)
    weight=models.FloatField(default=0.0)
    def addWeight(self,w):
        self.weight+=w
        self.project.addWeight(w)
        self.project.save()
        self.save()
    def __str__(self):
        return str(self.id)

class ReportToProject(models.Model):
    report=models.ForeignKey(Report,on_delete=models.CASCADE,default=None)
    project=models.ForeignKey(Project,on_delete=models.CASCADE,default=None)
    weight=models.FloatField(default=0.0)
    author=models.ForeignKey(Users,on_delete=models.CASCADE,default=None)
    pub_date=models.DateField(default=timezone.now)
    def __str__(self):
        return str(self.id)
