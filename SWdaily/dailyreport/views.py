# -*- coding:utf-8 -*-
from django.shortcuts import render,get_object_or_404
from .models import Users
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
# Create your views here.
import drviews

def index(request):
    if request.method=='GET':
        return drviewsiiews.index.getRequest(request)
    latest_user_list=Users.objects.order_by('id')
    #template=loader.get_template('dailyreport/index.html')
    context={
            'user_list':latest_user_list,
            }
    return render(request,'dailyreport/index.html',context)
    #return HttpResponse(template.render(context,request))


def detail(request,userid):
    try:
        if request.session['is_login']:
            #todo
            dt=get_object_or_404(Users,id=userid)
            return render(request,'dailyreport/detail.html',{'user':dt})

        else:
            return HttpResponseRedirect(reverse('dailyreport:detail',args=(request.session['user_id'],)))

    except KeyError:
        return HttpResponseRedirect(reverse('dailyreport:login')) 

def login(request):
    try:
        login_user=Users.objects.get(name=request.POST['username'])
    except(KeyError,Users.DoesNotExist):
        return render(request,'dailyreport/login.html',{
            'error_message':"没有此用户，请检查用户名",
            })
    else:
        password=request.POST['pwd']
        msg=""
        if check_password(password,login_user.password):
            msg="登陆成功"
            request.session['is_login']=True
            request.session['user_id']=login_user.id
            request.session['user_name']=login_user.name
            if password=="123456":
                return render(request,'dailyreport/changepassword.html',{
                    'error_message':request.session['user_name'],})
            else:
                return HttpResponseRedirect(reverse('dailyreport:main',args=(login_user.id,)))
        else:
            msg="密码错误"
            #MSG=HASh(password)
            #msg=password
            return render(request,'dailyreport/login.html',{
                'error_message':msg,
                })
def changePassword(request):
    try:
        if request.session['is_login']:
            pwd1=request.POST['pwd1']
            pwd2=request.POST['pwd2']
            if pwd1!=pwd2:

                return render(request,'dailyreport/changepassword.html',{
                    'error_message':"两次密码不一致",
                    })
            else:
                userid=request.session['user_id']
                a=Users.objects.get(id=userid)
                a.password=make_password(pwd1)
                a.save()

                return HttpResponseRedirect(reverse('dailyreport:main',args=(userid,)))
    except KeyError:
        return HttpResponseRedirect(reverse('dailyreport:login')) 
def main(request,userid):
    try:
        if request.session['is_login']:
            user=get_object_or_404(Users,id=userid)
            return render(request,'dailyreport/main.html',{
                'user':user,
                })
    except KeyError:
        return HttpResponseRedirect(reverse('dailyreport:login'))
