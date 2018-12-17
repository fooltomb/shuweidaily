# -*- coding:utf-8 -*-
from django.shortcuts import render,get_object_or_404
from dailyreport.models import Users
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse


def changePassword(request):
    if request.method=='GET':
        if request.session.get('is_login',False):
            return render(request,'dailyreport/changepassword.html',{
                'error_message':request.session['user_name'],})
        else:
            return HttpResponseRedirect(reverse('dailyreport:login'))
    if request .method=='POST':
        pwd1=request.POST['pwd1']
        pwd2=request.POST['pwd2']
        if pwd1!=pwd2:
            return render(request,'dailyreport/changepassword.html',{
                'error_message':'两次密码不一致',
                })
        else:
            userid=request.session['user_id']
            a=Users.objects.get(id=userid)
            a.password=make_password(pwd1)
            a.save()
            #TODO
            return HttpResponseRedirect(reverse('dailyreport:main'))

