# -*- coding:utf:8 -*-
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from dailyreport.models import Users,Project,Report,UserToProject,ReportToProject
from django.shortcuts import render,get_object_or_404
from django.utils import timezone


def searchProject(request):
    if not request.session['is_login']:
        return HttpResponseRedirect(reverse('dailyreport:login'))
    if request.method=='GET':
        project_list=Project.objects.all()
        return_list=[]
        for p in project_list:
            p_user=[""]
            p_weight=[p.name]
            u2p_list=UserToProject.objects.filter(project=p)
            for u2p in u2p_list:
                p_user.append(str(u2p.author))
                p_weight.append(u2p.weight)
            return_list.append([p_user,p_weight])
        return render(request,'dailyreport/project.html',{
            'return_list':return_list,
            'today':timezone.now(),
            'project_list':project_list,
            })

    if request.method=='POST':
        project_id=request.POST['project']
        begin_date=request.POST['begin_date']
        end_date=request.POST['end_date']
        project_list=Project.objects.all()
        temp=[]
        if project_id=="-1":
            temp=project_list
        else:
            temp=[Project.objects.get(id=project_id)]
        return_list=[]
        for project in temp:
            element=GetReturnElement(project,begin_date,end_date)
            if element!=None:
                return_list.append(element)
        return render(request,'dailyreport/project.html',{
            'return_list':return_list,
            'today':timezone.now(),
            'project_list':project_list,
            })

def GetReturnElement(project,begin_date,end_date):
    r2p_list=ReportToProject.objects.filter(project=project,pub_date__gte=begin_date,pub_date__lte=end_date)
    user_dict={}
    for r2p in r2p_list:
        if r2p.author in user_dict:
            user_dict[r2p.author]+=r2p.weight
        else:
            user_dict[r2p.author]=r2p.weight
    if len(user_dict)==0:
        return None
    p_user=[""]
    p_weight=[project.name]
    for key,value in user_dict.items():
        p_user.append(key)
        p_weight.append(value)
    return [p_user,p_weight]




