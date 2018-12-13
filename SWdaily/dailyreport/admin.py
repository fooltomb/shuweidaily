from django.contrib import admin

# Register your models here.
from .models import Users,Report,Project,ReportToProject


admin.site.register(Users)
admin.site.register(Report)
admin.site.register(Project)
admin.site.register(ReportToProject)
