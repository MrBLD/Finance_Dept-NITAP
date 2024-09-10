from django.urls import path
from . import views

app_name = 'SalarySlip'

urlpatterns = [
    # Add path here
    # User DashBoard
    path(route='', view=views.dashboard),
    path(route='dashboard', view=views.dashboard, name='dashboard'),

    # User Registration form the userside
    path(route='register', view=views.TeacherRegistration, name='register'),

    # Admin and User login
    path(route='login/', view=views.user_login, name='login'),

    # Upload and Reupload on the Admin Side
    path(route='upload', view=views.upload, name='upload'),

    # Monthly Report Page on User Side
    path(route='monthlyview', view=views.monthly_report, name='monthlyview'),

    # Dowload page on User Side
    path(route='download', view=views.download, name='download'),

    # Monthly Data view Page on Admin Side
    path(route='view', view=views.view, name='view'),

    # Logout Page
    path(route='logout/', view=views.log_out, name='logout'),

    # Admin Dashboard
    path(route='admin', view=views.admin, name='admin'),

    #Changepassword for Admin Side
    path(route='changepassword', view=views.changepassword, name='changepassword'),

    # Help Page for both Admin and User
    path(route='help', view=views.help, name='help'),

    # Admin Side Download Page
    path(route='slip', view=views.slipdownload, name='slipdownload'),

    # Excel View Page on the Admin side
    path(route='excel/<str:month>/<int:year>/', view=views.excelread, name='excelread'),
]
