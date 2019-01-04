# -*- coding:utf:8 -*-
from django.shortcuts import render,get_object_or_404
from dailyreport.models import Users
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect


def login(request):
    if request.method=='GET':
        return render(request,'dailyreport/login.html',{})
    if request.method=='POST':
        try:
            login_user=Users.objects.get(name=request.POST['username'])
        except (KeyError,Users.DoesNotExist):
            msg="没有此用户，请检查用户名"
            return render(request,'dailyreport/login.html',{
                'error_message':msg,
                })
        else:
            password=request.POST['pwd']
            if check_password(password,login_user.password):
                request.session['is_login']=True
                request.session['user_id']=login_user.id
                request.session['user_name']=login_user.name
                request.session['is_super']=login_user.superuser
                if password=="123456":
                    return render(request,'dailyreport/changepassword.html',{
                        'error_message':login_user.name,})
                else:
                    #TODO
                    return HttpResponseRedirect(reverse('dailyreport:main'))
            else:
                return render(request,'dailyreport/login.html',{
                    'error_message':'密码错误',})

def logout(request):
    request.session.clear()
    return HttpResponseRedirect(reverse('dailyreport:login'))

