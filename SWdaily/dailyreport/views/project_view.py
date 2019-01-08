# -*- coding:utf:8 -*-
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from dailyreport.models import Users,Project,Report,UserToProject,ReportToProject
from django.shortcuts import render,get_object_or_404
from django.utils import timezone
import json

def searchProject(request):
    if not request.session.get('is_login',False):
        return HttpResponseRedirect(reverse('dailyreport:login'))

    project_list=Project.objects.all()
    p_list=[]
    for pro in project_list:
        p_list.append([pro.id,pro.name,pro.detail,str(pro.start_date),str(pro.end_date),pro.isWorking,pro.reward])

    if request.method=='GET':
        return_list=[]
        for p in project_list:
            p_user=[""]
            p_weight=[p.name]
            u2p_list=UserToProject.objects.filter(project=p)
            sumOfWeight=0
            for u2p in u2p_list:
                sumOfWeight+=u2p.weight
                p_user.append(str(u2p.author))
                p_weight.append('%.1f'%u2p.weight)
            p_user.append("合计")
            p_weight.append('%.1f'%sumOfWeight)
            return_list.append([p_user,p_weight])
        return render(request,'dailyreport/project.html',{
            'return_list':return_list,
            'today':timezone.now(),
            'project_list':project_list,
            'is_super':request.session['is_super'],
            'p_list':json.dumps(p_list),
            })

    if request.method=='POST':
        project_id=request.POST['project']
        begin_date=request.POST['begin_date']
        end_date=request.POST['end_date']
        temp=[]
        if project_id=="-1":
            temp=project_list.filter(isWorking=True)
        elif project_id=="-2":
            temp=project_list.filter(isWorking=False)
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
            'is_super':request.session['is_super'],
            'p_list':json.dumps(p_list),
            })

def GetReturnElement(project,begin_date,end_date):
    if begin_date=="":
        begin_date="2015-05-24"
    if end_date=="":
        end_date=timezone.now()
    r2p_list=ReportToProject.objects.filter(project=project,pub_date__gte=begin_date,pub_date__lte=end_date)
    user_dict={}
    for r2p in r2p_list:
        user_dict[r2p.author]=0.0
    sumOfWeight=0.0
    for r2p in r2p_list:
        sumOfWeight+=r2p.weight
        user_dict[r2p.author]+=r2p.weight
    if len(user_dict)==0:
        return None
    p_user=[""]
    p_weight=[project.name]
    for key,value in user_dict.items():
        p_user.append(key)
        p_weight.append('%.1f'%value)
    p_user.append("合计")
    p_weight.append('%.1f'%sumOfWeight)
    return [p_user,p_weight]

def AddProject(request):
    if not request.session['is_login']:
        return HttpResponseRedirect(reverse('dailyreport:login'))
    if request.method=='GET':
        return HttpResponseRedirect(reverse('dailyreport:project'))

    if request.method=='POST':
        pro_id=request.POST['project']
        pro_name=request.POST['projectname']
        pro_detail=request.POST['projectdetail']
        begin_date=request.POST['begin_date']
        end_date=request.POST['end_date']
        pro_isWorking=request.POST['isworking']=="1"
        pro_reward=request.POST['reward']
        pro=""
        if pro_id=="-1":
            pro,created=Project.objects.get_or_create(name=pro_name)
            if not created:
                return HttpResponse("已存在同名项目，请修改项目名称")
        else:
            pro=Project.objects.get(id=pro_id)
            
            if pro.name!=pro_name:
                try:
                    Project.objects.get(name=pro_name)
                    return HttpResponse("已存在同名项目")
                except:
                    pro.name=pro_name
        pro.detail=pro_detail
        pro.start_date=begin_date
        pro.end_date=end_date
        pro.isWorking=pro_isWorking
        pro.reward=pro_reward
        pro.save()
        if pro_id=="-1":
            return HttpResponse("创建项目成功")
        else:
            return HttpResponse("修改项目成功")

def DeleteProject(request):
    if not request.session['is_login']:
        return HttpResponseRedirect(reverse('dailyreport:login'))
    if request.method=='GET':
        return render(request,'dailyreport/testdate.html',{})
        return HttpResponseRedirect(reverse('dailyreport:project'))
    if request.method=='POST':
        pro_id=request.POST["project"]
        pro=Project.objects.get(id=pro_id)
        name=pro.name
        ReportToProject.objects.filter(project=pro).delete()
        UserToProject.objects.filter(project=pro).delete()
        pro.delete()
        return HttpResponse(name+"已被删除")



