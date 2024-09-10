from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import check_password
import pandas as pd
from SalarySlip.models import Report, Teacher

#Global Variables
All_month = Report.objects.all()

#Creating all the functions

# Get name of all the teacher avialable
def getTeacherName():
    All_Teacher = Teacher.objects.all()
    teacher_name = []
    teacher_email = []
    for teacher in All_Teacher:
        name = teacher.get_full_name()
        EMAIL = teacher.getEmail()
        teacher_name.append(name)
        teacher_email.append(EMAIL)
    del All_Teacher
    return teacher_email, teacher_name

# Update All_month Global Variable
def Update_allmonth():
    global All_month
    data = Report.objects.all()
    All_month=data
    del data

# names of all the month avilable in database
def getAllExcelName():
    data = []
    for month in All_month:
        name = month.getName()
        data.append(name)
    month = [item.split('_')[0] for item in data]
    year = [item.split('_')[1] for item in data]
    data.clear()
    for i in range(len(month)):
        data.append({'month': month[i], 'year': year[i]})
    del year
    del month
    return data

# Create monthly view page for the User
def create_monthly_view(email):
    months_list =[]
    Total =[]
    for month in All_month:
        address = pd.ExcelFile(month.excel)
        df = pd.read_excel(address)
        if df['Email ID'].isin([email]).any():
            name = month.getName()
            months_list.append(name)
            totalSum = df.loc[df['Email ID'] == email, 'Net_Amount'].item()
            Total.append(totalSum)
    return Total, months_list

# Generate Html of the Excel Sheet of the given month and year
def GenerateExcel(month, year):
    Excel = Report.objects.get(month=month, year=year)
    excel_add = Excel.excel
    excel_data = pd.read_excel(excel_add)
    del excel_add
    excel_data_html = excel_data.to_html(index=False, classes="table table-bordered")
    del excel_data
    context = {'excel_data_html': excel_data_html}
    return context

# Check if the given data is presesnt
def IsPresent(month, year):
    new_name = month + '_' + year
    for month in All_month:
        name = month.getName()
        if name == new_name:
            return True
    return False

# Delete Excel Sheet of given month and year
def deleteData(month, year):
    given_name = month+'_'+year
    for month in All_month:
        if given_name == month.getName():
            month.delete()
            return True
    return False

# Get all the Data for specific month and year for Download page
def getData(email, month, year):
    Excel = Report.objects.get(month=month, year=year)
    address = Excel.excel
    df = pd.read_excel(address)
    if df['Email ID'].isin([email]).any():
        filtered_df = df[df['Email ID'] == email]
        del df
        columns_to_remove = ['Email ID','Net_Amount']
        filtered_df.drop(columns=columns_to_remove, inplace=True)
        excelData = filtered_df.to_dict(orient='records')
        excelData=excelData[0]
        del filtered_df
        excelData["Email_id"] = email
        excelData["month"] = month
        excelData["year"] = year
        return excelData
    else:
        return  None

# Create your views here.

# Monthly Report Page on User Side
def monthly_report(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        user = request.user
        teacher = Teacher.objects.get(user_ptr_id=user.id)
        Total, month_list = create_monthly_view(teacher.email)
        month = [item.split('_')[0] for item in month_list]
        year = [item.split('_')[1] for item in month_list]
        data = []
        for i in range(len(month)):
            data.append({'month': month[i], 'year': year[i], 'total': Total[i]})
        context = {'data': data}
        return render(request, 'MonthlyReport.html', context)
    else:
        logout(request)
        return redirect('SalarySlip:login')

# Upload and Reupload for the admin side
def upload(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method =='POST':
            if not 'myfile' in request.FILES:
                context = {
                        'error' : 'Please Choose a file'
                    }
                return render(request, 'upload_page.html', context)
            else:
                uploaded_file = request.FILES['myfile']
                month = request.POST['month']
                year = request.POST['year']
                if 'reup' in request.POST:
                    if IsPresent(month, year):
                        deleteData(month, year)
                        report = Report(month=month, year=year, excel=uploaded_file)
                        report.save()
                        context = {
                            'error' : 'deleted'
                        }
                        Update_allmonth()
                        return render(request, 'upload_page.html', context)
                    else:
                        context = {
                            'error' : 'File is not uploaded for the given month. Please Uncheck the box and Upload again '
                        }
                        return render(request, 'upload_page.html', context)
                else:
                    if IsPresent(month, year):
                        context = {
                            'error' : 'File is already is uploaded for the given month Please tick the checkbox and reupload again'
                        }
                        return render(request, 'upload_page.html', context)
                    else:
                        report = Report(month=month, year=year, excel=uploaded_file)
                        report.save()
                        context = {
                            'error' : 'Uploaded'
                        }
                        Update_allmonth()
                        return render(request, 'upload_page.html', context)
        else:
            return render(request, 'upload_page.html')
    else:
        logout(request)
        return redirect('SalarySlip:login')

# Teacher Registration for the Admin
def TeacherRegistration(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            fn = request.POST['first_name']
            ln = request.POST['last_name']
            em = request.POST['email']
            psw = request.POST['pwd']
            degisnation = request.POST['degisnation']
            try:
                instance = Teacher(username = em, password=make_password(psw) , first_name =fn, last_name = ln, email=em, Degisnation=degisnation)
                instance.save()
                error = 'User Created'
            except IntegrityError:
                error = 'Somethink went wrong, Either Email or Employee Id is not unique. Try putting the unique Email or EmpId'
            context = {
                'error' : error,
            }
            return render(request, 'create_teacher.html', context)
        else:
            return render(request, 'create_teacher.html')
    else:
        logout(request)
        return redirect('SalarySlip:login')

# User side Download Page
def download(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        user = request.user
        if request.method =='POST':
            month = request.POST['month']
            year = request.POST['year']
            teacher = Teacher.objects.get(user_ptr_id=user.id)
            emailId = teacher.email
            context = getData(emailId, month, year)
            if(context!=None):
                return render(request, 'SalarySlip.html', context)
            else:
                message = 'Sorry No data for found, make sure that your data of this month is available in Monthly Report.'
                context = {
                    'error' : message,
                }
                return render(request, 'download.html', context)
        else:
            return render(request, 'download.html')
    else:
        logout(request)
        return redirect('SalarySlip:login')

# Download Page for the Admin Side
def slipdownload(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method =='POST':
            month = request.POST['month']
            year = request.POST['year']
            email = request.POST['teacher']
            context = getData(email, month, year)
            if(context!=None):
                print(context)
                return render(request, 'SalarySlip.html', context)
            else:
                message = 'Sorry No data for found, make sure that your data of this month is available in Monthly Report.'
                email, name = getTeacherName()
                data = []
                for i in range(len(email)):
                    data.append({'name': name[i], 'id': email[i]})
                context = {'data': data,'error' : message}
                del data
                return render(request, 'admindownload.html', context)
        else:
            email, name = getTeacherName()
            data = []
            for i in range(len(email)):
                data.append({'name': name[i], 'id': email[i]})
            context = {'data': data}
            del data
            return render(request, 'admindownload.html', context)
    else:
        logout(request)
        return redirect('SalarySlip:login')

# Password change for the users
def changepassword(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        user = request.user
        if request.method == 'POST':
            opsw = request.POST['o_pwd']
            psw = request.POST['pwd']
            if check_password(opsw, user.password):
                user.set_password(psw)
                user.save()
                logout(request)
                message = 'The Password has been changed successfully'
                context = {
                    'message' : message,
                }
                return redirect('/dashboard', context)
            else:
                message = 'Either Email is not unique. Try putting the unique Email'
                context = {
                    'message' : message,
                }
                return render(request, 'changepass.html', context)
        else:
            return render(request, 'changepass.html')
    else:
        logout(request)
        return redirect('/changepassword')

# Excel view page on Admin Side
def excelread(request, year, month):
    if request.user.is_authenticated and request.user.is_superuser:
        context = GenerateExcel(month, year)
        return render(request, 'excel.html', context)
    else:
        logout(request)
        return redirect('SalarySlip:login')

# Monthly Data view Page on Admin Side
def view(request):
    if request.user.is_authenticated and request.user.is_superuser:
        data = getAllExcelName()
        context = {'data': data}
        return render(request, 'view.html', context)
    else:
        logout(request)
        return redirect('SalarySlip:login')

# Admin Dashboard
def admin(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request, 'admin.html')
    else:
        logout(request)
        return redirect('SalarySlip:login')

# Dashboard for the user
def dashboard(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        user = request.user
        teacher = Teacher.objects.get(user_ptr_id=user.id)
        if teacher is not None:
            return render(request, 'dashboard.html')
        else:
            logout(request)
            return redirect('SalarySlip:login')
    elif request.user.is_authenticated and request.user.is_superuser:
        return redirect('SalarySlip:admin')
    else:
        logout(request)
        return redirect('SalarySlip:login')

# Login page
def user_login(request):
    if request.method == 'POST':
        un = request.POST['email']
        psw = request.POST['pwd']

        user = authenticate(request, username = un, password = psw)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('/admin')
            else:
                return redirect('/dashboard')
        else: 
            context={
                'error' : 'Invalid Username or pasword' 
            }
            return render(request, 'login.html', context)
    else: 
        return render(request, 'login.html')

# TODO: Update help page
# Help page for both admin and user
def help(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'help_page_admin.html')
        else:
            return render(request, 'help_page.html')
    else:
        return redirect('SalarySlip:login')

# Log out Button
def log_out(request):
    logout(request)
    return redirect('/login')
