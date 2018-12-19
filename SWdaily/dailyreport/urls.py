from django.urls import path
#import views.index_view as index_view
from dailyreport.views import index_view,login_view,changepassword_view,main_view,user_view,project_view


app_name='dailyreport'

urlpatterns=[
        path('',index_view.index,name='index'),
               
        path('login/',login_view.login,name='login'),
        path('login/changepwd/',changepassword_view.changePassword,name='changepassword'),
        path('main/',main_view.main,name='main'),
        path('project/',project_view.searchProject,name='project'),
        path('user/',user_view.searchUser,name='users'),
        path('adduser/',user_view.addUser,name='adduser'),
        ]

