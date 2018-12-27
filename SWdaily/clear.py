# -*- coding:utf-8 -*-
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE","SWdaily.settings")

import django
django.setup()
import xlrd
from dailyreport.models import Users,Project,Report,UserToProject,ReportToProject
def main():
    ReportToProject.objects.all().delete()
    UserToProject.objects.all().delete()
    Report.objects.all().delete()
    ps=Project.objects.all()
    for p in ps:
        p.spend_weight=0.0
        p.save()

if __name__=="__main__":
    main()

