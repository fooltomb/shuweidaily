# -*- coding:utf:8 -*-
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from dailyreport.models import Users,Project,Report,UserToProject
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



    return HttpResponse("do later")

