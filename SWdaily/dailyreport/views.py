# -*- coding:utf-8 -*-
from django.shortcuts import render,get_object_or_404
from .models import Users
# Create your views here.
def index(request):
    latest_user_list=Users.objects.order_by('id')
    #template=loader.get_template('dailyreport/index.html')
    context={
            'user_list':latest_user_list,
            }
    return render(request,'dailyreport/index.html',context)
    #return HttpResponse(template.render(context,request))


def datetime(request,userid):
    dt=get_object_or_404(Users,userid=userid)
    return render(request,'dailyreport/detail.html',{'user':dt})

def login(request):
    try:
        login_user=Users.objects.get(name=request.POST['username'])
    except(KeyError,Users.DoesNotExist):
        return render(request,'dailyreport/login.html',{
            'error_message':"没有此用户，请检查用户名",
            })
    else:
        msg=""
        if login_user.password==hash(request.POST['pwd']):
            msg="登陆成功"
        else:
            msg=hash(request.POST['pwd'])
        return render(request,'dailyreport/login.html',{
            'error_message':msg,
            })
