from django.urls import path
from . import views

app_name='dailyreport'

urlpatterns=[
        path('',views.index,name='index'),
        
        path('login/',views.login,name='login'),
        path('login/changepwd/',views.changePassword,name='changepassword'),
        path('detail/<userid>/',views.detail,name='detail'),
        path('main/<userid>/',views.main,name='main'),
        ]

