# -*- coding:utf-8 -*-
from django.shortcuts import render,get_object_or_404
from dailyreport.models import Users,Report,Project,UserToProject,ReportToProject
from dailyreport.forms import WriteReportForm
from django.http import HttpResponseRedirect,HttpResponse

from django.urls import reverse
from django.utils import timezone

def main(request):
    if request.method=='GET':
        if request.session.get('is_login',False):
            a=get_object_or_404(Users,id=request.session['user_id'])
            reportlist=Report.objects.filter(author=a).order_by('-pub_date')[:5]
            projectlist=Project.objects.filter(isWorking=True)
            form=WriteReportForm()
            return render(request,'dailyreport/main.html',{
                'user':a,'report_list':reportlist,
                'project_list':projectlist,
                'today':timezone.now(),
                'form':form,
                })
        else:
            return HttpResponseRedirect(reverse('dailyreport:login'))
    if request.method=='POST':
        a=get_object_or_404(Users,id=request.session['user_id'])
        pub_date=request.POST['pub_date']
        pro1_id=request.POST['project1']
        pro1_weight=request.POST['weight1']
        pro2_id=request.POST['project2']
        pro2_weight=request.POST['weight2']
        pro3_id=request.POST['project3']
        pro3_weight=request.POST['weight3']
        detail=request.POST['detail']
        sumOfWeight=float(pro1_weight)+float(pro2_weight)+float(pro3_weight)
        if sumOfWeight>1.0001 or sumOfWeight<0.99999:
            return HttpResponse("三个项目贡献之和不等于1，请返回重写")
        report,created=Report.objects.get_or_create(author=a,pub_date=pub_date)
        if not created:
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

        p1=Project.objects.get(id=pro2_id)
        u2p1,c=UserToProject.objects.get_or_create(author=a,project=p1)
        u2p1.addWeight(float(pro2_weight))
        report.project2=str(p1)
        ReportToProject.objects.create(report=report,project=p1,weight=pro2_weight,author=a,pub_date=pub_date)

        p1=Project.objects.get(id=pro1_id)
        u2p1,c=UserToProject.objects.get_or_create(author=a,project=p1)
        u2p1.addWeight(float(pro1_weight))
        report.project1=str(p1)
        ReportToProject.objects.create(report=report,project=p1,weight=pro1_weight,author=a,pub_date=pub_date)

        p1=Project.objects.get(id=pro3_id)
        u2p1,c=UserToProject.objects.get_or_create(author=a,project=p1)
        u2p1.addWeight(float(pro3_weight))
        report.project3=str(p1)

        ReportToProject.objects.create(report=report,project=p1,weight=pro3_weight,author=a,pub_date=pub_date)
        report.detail=detail
        report.weight1=pro1_weight
        report.weight2=pro2_weight
        report.weight3=pro3_weight
        report.save()
        
        return HttpResponseRedirect(reverse('dailyreport:main'))
