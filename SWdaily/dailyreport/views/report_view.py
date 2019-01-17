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
            'user':a,
            'report_list':[[a,reportlist]],
            'user_list':userlist,
            'today':timezone.now(),
            'is_super':request.session['is_super'],
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
            'user':request.session['user_name'],
            'report_list':return_list,
            'user_list':Users.objects.filter(active=True),
            'today':timezone.now(),
            'is_super':request.session['is_super'],
            })

def DeleteReport(request):
    if not request.session.get('is_login',False):
        return HttpResponseRedirect(reverse('dailyreport:login'))
    if request.method=='GET':
        return HttpResponseRedirect(reverse('dailyreport:report'))
    if request.method=='POST':
        try:
            a=Users.objects.get(id=request.POST['user'])
            date=request.POST['del_date']
            report=Report.objects.get(author=a,pub_date=date)
            if float(report.weight1)>0:
                p1=Project.objects.get(name=report.project1)
                u2p1=UserToProject.objects.get(author=a,project=p1)
                u2p1.addWeight(-float(report.weight1))
                if u2p1.weight<=0:
                    u2p1.delete()
            if float(report.weight2)>0:
                p1=Project.objects.get(name=report.project2)
                u2p1=UserToProject.objects.get(author=a,project=p1)
                u2p1.addWeight(-float(report.weight2))
                if u2p1.weight<=0:
                    u2p1.delete()
            if float(report.weight3)>0:
                p1=Project.objects.get(name=report.project3)
                u2p1=UserToProject.objects.get(author=a,project=p1)
                u2p1.addWeight(-float(report.weight3))
                if u2p1.weight<=0:
                    u2p1.delete()
            ReportToProject.objects.filter(report=report).delete()
            report.delete()
            return HttpResponse("员工"+a.name+"的"+date+"日报已被删除")
        except:
            return HttpResponse("无法查询到此日报，请检查输入")


