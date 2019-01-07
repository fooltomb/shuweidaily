# -*- coding:utf-8 -*-
from django.shortcuts import render,get_object_or_404
from dailyreport.models import Users,Report,Project,UserToProject,ReportToProject
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.utils import timezone

def searchReport(request):
    if not request.session.get('is_login',False):
        return HttpResponseRedirect(reverse('dailyreport:login'))
    if request.method=='GET':
        userlist=Users.objects.filter(active=True)
        a=get_object_or_404(Users,id=request.session['user_id'])
        reportlist=Report.objects.filter(author=a).order_by('pub_date')[:30]
        return render(request,'dailyreport/report.html',{
            'report_list':[[a,reportlist]],
            'user_list':userlist,
            'today':timezone.now(),
            })
    if request.method=='POST':
        return_list=[]
        user_id=request.POST['user']
        if user_id=="-1":
            users=Users.objects.filter(active=True)
            for u in users:
                return_list.append([u])
        else:
            u=Users.objects.get(id=user_id)
            return_list.append([u])
        begin_date=request.POST['begin_date']
        end_date=request.POST['end_date']
        for rp in return_list:
            if begin_date=="":
                begin_date="2015-05-24"
            if end_date=="":
                end_date=timezone.now()
            reportlist=Report.objects.filter(author=rp[0],pub_date__gte=begin_date,pub_date__lte=end_date)
            rp.append(reportlist)

        return render(request,'dailyreport/report.html',{
            'report_list':return_list,
            'user_list':Users.objects.filter(active=True),
            'today':timezone.now(),
            })


