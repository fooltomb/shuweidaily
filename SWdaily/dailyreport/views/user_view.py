# -*- conding:utf:8 -*-
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from dailyreport.models import Users,Project,UserToProject,Report
from django.shortcuts import render,get_object_or_404
from django.utils import timezone
from django.contrib.auth.hashers import make_password

def searchUser(request):
    if not request.session['is_login']:
        return HttpResponseRedirect(reverse('dailyreport:login'))

    if request.method=='GET':
        user_list=Users.objects.filter(active=True)
        rl=[]
        for u in user_list:
            u_project=[""]
            u_weight=[u.name]

            u2p_list=UserToProject.objects.filter(author=u)
            for u2p in u2p_list:
                u_project.append(str(u2p.project))
                u_weight.append(u2p.weight)
            rl.append([u_project,u_weight])
        return render(request,'dailyreport/user.html',{
            'list':rl,
            'today':timezone.now(),
            'user_list':user_list,
            'is_super':request.session['is_super'],
            })
    if request.method=='POST':
        user_id=request.POST['user']
        begin_date=request.POST['begin_date']
        end_date=request.POST['end_date']
        user_list=Users.objects.filter(active=True)
        temp=[]
        if user_id=="-1":
            temp=user_list
        else:
            temp=[Users.objects.get(id=user_id)]
        return_list=[]
        for user in temp:
            return_list.append(GetReturnElement(user,begin_date,end_date))
        return render(request,'dailyreport/user.html',{
            'list':return_list,
            'today':timezone.now(),
            'user_list':user_list,
            'is_super':request.session['is_super'],
            })


def GetReturnElement(user,begin_date,end_date):
    report_list=Report.objects.filter(author=user,pub_date__gte=begin_date,pub_date__lte=end_date)
    project_dict={}
    for report in report_list:
        if report.project1 in project_dict:
            project_dict[report.project1]+=report.weight1
        else:
            project_dict[report.project1]=report.weight1
        if report.project2 in project_dict:
            project_dict[report.project2]+=report.weight2
        else:
            project_dict[report.project2]=report.weight2
        if report.project3 in project_dict:
            project_dict[report.project3]+=report.weight3
        else:
            project_dict[report.project3]=report.weight3
    u_project=[""]
    u_weight=[user.name]
    for key,value in project_dict.items():
        u_project.append(key)
        u_weight.append(value)
    return [u_project,u_weight]

def addUser(request):
    if request.method=='GET':
        return HttpResponseRedirect(reverse('dailyreport:users'))
    if request.method=='POST':
        op=request.POST['option']
        if op=="addnew":
            obj,created=Users.objects.get_or_create(name=request.POST['newuser'])
            str="已增加新员工"+request.POST['newuser'] if created else "已有同名员工存在，请换个姓名"
            return HttpResponse(str)
        a=Users.objects.get(id=request.POST['user'])
        if op=="reset":
            a.password=make_password('123456')
            a.save()
            return HttpResponse("重制"+a.name+"的密码，新密码:123456")
        elif op=="unactive":
            a.active=False
            a.save()
            return HttpResponse("已将员工"+a.name+"设置为离职")



