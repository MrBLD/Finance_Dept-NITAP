from django.urls import path
from . import views

app_name = 'SalarySlip'

urlpatterns = [
    # Add path here
    path(route='', view=views.dashboard),
    path(route='dashboard', view=views.dashboard),
    path(route='dashboard', view=views.dashboard, name='dashboard'),
    
    path(route='register', view=views.TeacherRegistration),
    path(route='register', view=views.TeacherRegistration, name='register'),
    
    path(route='login/', view=views.user_login,),
    path(route='login/', view=views.user_login, name='login'),
    
    path(route='upload', view=views.upload),
    path(route='upload', view=views.upload, name='upload'),

    path(route='monthlyview', view=views.monthly_report),
    path(route='monthlyview', view=views.monthly_report, name='monthlyview'),
    
    path(route='download', view=views.download),
    path(route='download', view=views.download, name='download'),

    path(route='view', view=views.view),
    path(route='view', view=views.view, name='view'),

    path(route='logout/', view=views.log_out), 
    path(route='logout/', view=views.log_out, name='logout'),

    path(route='admin', view=views.admin),
    path(route='admin', view=views.admin, name='admin'),

    path(route='changepassword', view=views.changepassword),
    path(route='changepassword', view=views.changepassword, name='changepassword'),

    path(route='help', view=views.help),
    path(route='help', view=views.help, name='help'),

    path(route='excel/<str:month>/<int:year>/', view=views.excelread),
]
