# -*- coding:utf-8 -*-
import sys
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","SWdaily.settings")

import django
django.setup()
import xlrd
from dailyreport.models import Users,Project,Report,UserToProject,ReportToProject

def main(path):
    book=xlrd.open_workbook(path)
    sheet=book.sheet_by_index(0)
    colcount=sheet.ncols
    rowcount=sheet.nrows
    index=1
    while index<colcount and sheet.cell(4,index).value!="":
        date=sheet.cell(4,index).value
        print(date)
        date=xlrd.xldate.xldate_as_datetime(date,0)
        print(date)
        rowindex=6
        while rowindex<rowcount and sheet.cell(rowindex,0).value!="":
            userName=sheet.cell(rowindex,0).value.strip()
            if userName=="阿斯根":
                userName="阿思根"
            proName1=sheet.cell(rowindex,index).value.strip()
            if proName1=="":
                print(rowindex,index)
                rowindex+=3
                continue
            weight1=sheet.cell(rowindex,index+1).value
            if weight1=="":
                weight1=0.0
            proName2=sheet.cell(rowindex+1,index).value.strip()
            weight2=sheet.cell(rowindex+1,index+1).value
            if weight2=="":
                weight2=0.0
            proName3=sheet.cell(rowindex+2,index).value.strip()
            weight3=sheet.cell(rowindex+2,index+1).value
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

            rowindex+=3
        index+=2

if __name__=="__main__":
    arg=sys.argv[1]
    main(arg)
