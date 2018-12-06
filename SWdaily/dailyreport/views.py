# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Users
# Create your views here.
def index(request):
    latest_user_list=Users.objects.order_by('id')
    template=loader.get_template('dailyreport/index.html')
    context={
            'user_list':latest_user_list,
            }

    return HttpResponse(template.render(context,request))

def names(request,userid):
    return HttpResponse("试一试中文显示:%s"%userid)
