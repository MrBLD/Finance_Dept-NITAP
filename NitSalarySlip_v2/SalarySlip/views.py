from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import check_password
import pandas as pd
from SalarySlip.models import Report, Teacher

#Global Variables
All_month = Report.objects.all()
global_Total = []
globalV = False
globalId = 0
global_months_list = []

def convert_allmonth(data):
    All_month=data


def creatingmonthly(id):
    global globalV
    global globalId
    for month in All_month:
        address = pd.ExcelFile(month.excel)
        df = pd.read_excel(address)
        if df['Employee ID'].isin([id]).any():
            name = month.getName()
            global_months_list.append(name)
            totalSum = df.loc[df['Employee ID'] == id, 'Net_Amount'].item()
            global_Total.append(totalSum)
            globalId = id
            globalV = True
    # return Total, months_list
    
# Creating Functions

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
    return data

def create_monthly_view(id):
    months_list =[]
    Total =[]
    for month in All_month:
        address = pd.ExcelFile(month.excel)
        df = pd.read_excel(address)
        if df['Employee ID'].isin([id]).any():
            name = month.getName()
            months_list.append(name)
            totalSum = df.loc[df['Employee ID'] == id, 'Net_Amount'].item()
            Total.append(totalSum)
    return Total, months_list

def GenerateExcel(month, year):
    print(month)
    print(year)
    Excel = Report.objects.get(month=month, year=year)
    excel_add = Excel.excel
    excel_data = pd.read_excel(excel_add)
    excel_data_html = excel_data.to_html(index=False, classes="table table-bordered")
    context = {'excel_data_html': excel_data_html}
    return context

def Present(month, year):    
    new_name = month + '_' + year
    for month in All_month:
        name = month.getName()
        if name == new_name:
            return True 
    return False

def deleteData(month, year):
    given_name = month+'_'+year
    for month in All_month:
        if given_name == month.getName():
            month.delete()
            return True
    return False

def getData(id, month, year):
    Excel = Report.objects.get(month=month, year=year)
    address = Excel.excel
    df = pd.read_excel(address)
    if df['Employee ID'].isin([id]).any():
        filtered_df = df[df['Employee ID'] == id]
        print(1)
        print(filtered_df)
        del df
        columns_to_remove = ['Employee ID', 'Name','Net_Amount']
        filtered_df.drop(columns=columns_to_remove, inplace=True)
        ans = filtered_df.to_dict(orient='records')
        print(2)
        print(filtered_df)
        del filtered_df
        ans['Emp_id'] = id
        ans['month'] = month
        ans['year'] = year
        return ans
    else:
        return  None


# Create your views here.

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

def help(request):
    print(type(All_month))
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'help_page_admin.html')
        else:
            return render(request, 'help_page.html')
    else:
        return redirect('SalarySlip:login')

def monthly_report(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        user = request.user
        teacher = Teacher.objects.get(user_ptr_id=user.id)
        emp_id = teacher.Employee_id
        Total, month_list = create_monthly_view(emp_id)
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

# def monthly_report(request):
#     if request.user.is_authenticated and not request.user.is_superuser:
#         user = request.user
#         teacher = Teacher.objects.get(user_ptr_id=user.id)
#         emp_id = teacher.Employee_id
#         if(emp_id==globalId and globalV):    
#             month = [item.split('_')[0] for item in month_list]
#             year = [item.split('_')[1] for item in month_list]
#             data = []
#             for i in range(len(month)):
#                 data.append({'month': month[i], 'year': year[i], 'total': Total[i]})
#             context = {'data': data}
#             return render(request, 'MonthlyReport.html', context)
#     else:
#         logout(request)
#         return redirect('SalarySlip:login')

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
                    if Present(month, year):
                        deleteData(month, year)
                        report = Report(month=month, year=year, excel=uploaded_file)
                        report.save()
                        context = {
                            'error' : 'deleted'
                        }
                        data=Report.objects.all()
                        convert_allmonth(data)
                        return render(request, 'upload_page.html', context)
                    else:
                        print('in reuploading data not found')
                        context = {
                            'error' : 'File is not uploaded for the given month. Please Uncheck the box and Upload again '
                        }
                        return render(request, 'upload_page.html', context)
                else:
                    if Present(month, year):
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
                        data=Report.objects.all()
                        convert_allmonth(data)
                        return render(request, 'upload_page.html', context)
        else:
            return render(request, 'upload_page.html')
    else:
        logout(request)
        return redirect('SalarySlip:login')

def TeacherRegistration(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            Emp_id = request.POST['id']
            fn = request.POST['first_name']
            ln = request.POST['last_name']
            em = request.POST['email']
            psw = request.POST['pwd']
            degisnation = request.POST['degisnation']
            try:
                instance = Teacher(username = em, password=make_password(psw) , Employee_id=Emp_id, first_name =fn, last_name = ln, email=em, Degisnation=degisnation)
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

def log_out(request):
    logout(request)
    return redirect('/login')

def admin(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request, 'admin.html')
    else:
        logout(request)
        return redirect('SalarySlip:login')

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
                message = 'Either Email or Employee Id is not unique. Try putting the unique Email or EmpId'
                context = {
                    'message' : message,
                }
                return render(request, 'changepass.html', context)
        else:
            return render(request, 'changepass.html')
    else:
        logout(request)
        return redirect('/changepassword')

def download(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        user = request.user
        if request.method =='POST':
            month = request.POST['month']
            year = request.POST['year']
            teacher = Teacher.objects.get(user_ptr_id=user.id)
            id = teacher.Employee_id
            context = getData(id, month, year)
            if(context!=None):
                print(context)
                return render(request, 'SalarySlip2.html', context)
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

def view(request):
    if request.user.is_authenticated and request.user.is_superuser:
        data = getAllExcelName()
        context = {'data': data}
        return render(request, 'view.html', context)
    else:
        logout(request)
        return redirect('SalarySlip:login')

def excelread(request, year, month):
    if request.user.is_authenticated and request.user.is_superuser:
        context = GenerateExcel(month, year)
        return render(request, 'excel.html', context)
    else:
        logout(request)
        return redirect('SalarySlip:login')
    