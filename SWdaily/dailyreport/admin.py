from django.contrib import admin

# Register your models here.
from .models import Users,Report,Project,UserToProject,ReportToProject


admin.site.register(Users)
admin.site.register(Report)
admin.site.register(Project)
admin.site.register(UserToProject)
admin.site.register(ReportToProject)
