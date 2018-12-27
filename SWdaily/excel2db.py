# -*- coding:utf-8 -*-
import sys
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","SWdaily.settings")

import django
django.setup()
import xlrd
from dailyreport.models import Users,Project,Report,UserToProject,ReportToProject
def main(path):
    book=xlrd.open_workbook(path)#mportData/04.xlsx')
    sheet=book.sheet_by_index(0)
    rowcount=sheet.nrows
    index=1
    while index<rowcount and sheet.cell(index,0).value!="":

        print(index)
        date=sheet.cell(index,0).value
        date=xlrd.xldate.xldate_as_datetime(date,0)
        userName=sheet.cell(index,1).value.strip()
        if userName=="阿斯根":
            userName="阿思根"
        if userName=="张慧":
            userName="张惠"
        proName1=sheet.cell(index,2).value.strip()
        weight1=sheet.cell(index,3).value
        if weight1=="":
            weight1=0.0
        proName2=sheet.cell(index+1,2).value.strip()
        weight2=sheet.cell(index+1,3).value
        if weight2=="":
            weight2=0.0
        proName3=sheet.cell(index+2,2).value.strip()
        #print(proName3)
        weight3=sheet.cell(index+2,3).value
        if weight3=="":
            weight3=0.0
        a=Users.objects.get(name=userName)
        report,created=Report.objects.get_or_create(author=a,pub_date=date,detail="")
        if not created:
            p1=Project.objects.get(name=report.project1)
            u2p1=UserToProject.objects.get(author=a,project=p1)
            u2p1.addWeight(-float(report.weight1))

            p2=Project.objects.get(name=report.project2)
            u2p2=UserToProject.objects.get(author=a,project=p2)
            u2p2.addWeight(-float(report.weight2))

            p3=Project.objects.get(name=report.project3)
            u2p3=UserToProject.objects.get(author=a,project=p3)
            u2p3.addWeight(-float(report.weight3))

            ReportToProject.objects.filter(report=report).delete()
        p1=Project.objects.get(name=proName1)
        u2p1,c=UserToProject.objects.get_or_create(author=a,project=p1)
        u2p1.addWeight(float(weight1))
        report.project1=str(p1)
        ReportToProject.objects.create(report=report,project=p1,weight=weight1,author=a,pub_date=date)

        p2=Project.objects.get(name=proName2)
        u2p2,c=UserToProject.objects.get_or_create(author=a,project=p2)
        u2p2.addWeight(float(weight2))
        report.project2=str(p2)
        ReportToProject.objects.create(report=report,project=p2,weight=weight2,author=a,pub_date=date)

        p3=Project.objects.get(name=proName3)
        u2p3,c=UserToProject.objects.get_or_create(author=a,project=p3)
        u2p3.addWeight(float(weight3))
        report.project3=str(p3)
        ReportToProject.objects.create(report=report,project=p3,weight=weight3,author=a,pub_date=date)

        report.detail=""
        report.weight1=weight1
        report.weight2=weight2
        report.weight3=weight3
        report.save()

        index+=3





if __name__=="__main__":
    #main()
    arg=sys.argv[1]
    print(arg)
    main(arg)
