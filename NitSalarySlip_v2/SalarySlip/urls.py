from django.urls import path
from . import views

app_name = 'SalarySlip'

urlpatterns = [
    # Add path here
    path(route='', view=views.dashboard),
    path(route='homepage', view=views.user_login),
    path(route='dashboard', view=views.dashboard),
    path(route='register', view=views.TeacherRegistration),
    path(route='login/', view=views.user_login, name='login'),
    path(route='upload', view=views.upload),
    path(route='monthlyview', view=views.monthly_report),
    path(route='download', view=views.download),
    path(route='view', view=views.view),
    path(route='logout/', view=views.log_out),
    path(route='Teacher_register', view=views.TeacherRegistration),
    path(route='admin', view=views.admin),
    path(route='changepassword', view=views.changepassword),
    path(route='help', view=views.help),
    path(route='excel/<str:month>/<int:year>/', view=views.excelread),
]