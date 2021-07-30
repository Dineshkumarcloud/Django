##### Import Packages ######
from django.core import paginator
from django.shortcuts import render
from django.http import HttpResponse, request, response
from datetime import date, datetime
from django.utils.encoding import smart_bytes

from pandas.core.indexes.datetimes import date_range
from home.models import sms_eva_Model
from home.models import netbanking_Model
import xlwt
import json
import pandas as pd
from io import BytesIO as IO
from django.core.paginator import Paginator
from django.http import StreamingHttpResponse
from django.db.models import Q
import dateutil.parser
from django.utils.dateformat import DateFormat

from django_globals import globals

from django.core import serializers

# Create your views here.


TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR, "templates")'
)


def index(request):
    today = datetime.datetime.now().date()
    return render(request, "index.html", {"today": today})



def smseva(request):
    #print("branch_code check:::",request.POST.dict)
    global cust_id,branch_id,from_date,to_date,ch_smseva
    
    cust_id = request.POST.get('Customer_ID')
    branch_id = request.POST.get('Branch_Code')
    ch_smseva = request.POST.get("choose-channel-select")=="smseva"
    #from_date = request.POST.get('fromdate')
    #to_date= request.POST.get('todate')
    #print("from_date and to_date::::::",from_date,to_date)
    #print("type_check",type(from_date),type(to_date))


    if (request.method =="POST" and request.POST.get('Branch_Code')):
        #global branch_code
        branch_code = request.POST.get('Branch_Code')

        #branch_code = request.POST.get('Branch_Code')
        smseva_query =f"""select pseudoId, pcId, mobilenumber, current_category, eligible_category, consent_of_user, consent_time, CustomerName, existing_branch, change_branch, change_rm,employee_code, state, city, branch, branch_code, existing_branch_code, sessionID, IPaddress, channel_remarks, device from smseva where branch_code={branch_code} or existing_branch_code= {branch_code}"""
        netbank_query=f"""select Sr_No,Promo_code,Cust_Id ,Customer_Name ,Eligible_Programme ,Account_no,Home_BranchName ,Home_BranchCode,CR_programme_RM_Change ,Credit_Card ,DC_Upgrade ,Selected_Branchname,Selected_Branchcode,Employee_Code ,Confirmation_authorize ,IP_Address ,Session_Id ,User_Agent,Lead_Date ,Confirmation_Authorize_for_Debit_Card,Confirmation_Authorize_for_Credit_Card from netbank where Home_BranchCode = {branch_code} or Selected_Branchcode = {branch_code}"""
        smseva_output = sms_eva_Model.objects.raw(smseva_query)
        netbank_output = netbanking_Model.objects.raw(netbank_query)        
        return render(request,'index.html',{"smseva":smseva_output,"netbank":netbank_output})

    
    elif (request.method =="POST" and request.POST.get('fromdate') and  request.POST.get('todate')):
        #global fromdate,todate
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        smseva_query =f"""select pseudoId, pcId, mobilenumber, current_category, eligible_category, consent_of_user, consent_time, CustomerName, existing_branch, change_branch, change_rm,employee_code, state, city, branch, branch_code, existing_branch_code, sessionID, IPaddress,channel_remarks, device from smseva where convert(date,consent_time)  between '{fromdate}'  and '{todate}' """
        netbank_query= f"""select Sr_No,Promo_code,Cust_Id, Customer_Name ,Eligible_Programme ,Account_no,Home_BranchName ,Home_BranchCode,CR_programme_RM_Change ,Credit_Card ,DC_Upgrade ,Selected_Branchname,Selected_Branchcode,Employee_Code ,Confirmation_authorize ,IP_Address ,Session_Id ,User_Agent,Lead_Date ,Confirmation_Authorize_for_Debit_Card,Confirmation_Authorize_for_Credit_Card from netbank where convert(date,Lead_Date)  between '{fromdate}' and '{todate}'"""
        smseva_output = sms_eva_Model.objects.raw(smseva_query)
        netbank_output = netbanking_Model.objects.raw(netbank_query)
        return render(request,'index.html',{"smseva":smseva_output,"netbank":netbank_output})


    elif (request.method =="POST" and request.POST.get('Customer_ID')):
        #print("check customer_id::::::::::",request.POST.get())
        #global customer_id

        customer_id = request.POST.get('Customer_ID')
        smseva_query =f"""select pseudoId, pcId, mobilenumber, current_category, eligible_category, consent_of_user, consent_time, CustomerName, existing_branch, change_branch, change_rm,employee_code, state, city, branch, branch_code, existing_branch_code, sessionID, IPaddress, channel_remarks, device from smseva where pcId = {customer_id} """
        netbank_query=f"""select Sr_No,Promo_code,Cust_Id ,Customer_Name ,Eligible_Programme ,Account_no,Home_BranchName ,Home_BranchCode,CR_programme_RM_Change ,Credit_Card ,DC_Upgrade ,Selected_Branchname,Selected_Branchcode,Employee_Code ,Confirmation_authorize ,IP_Address ,Session_Id ,User_Agent,Lead_Date ,Confirmation_Authorize_for_Debit_Card,Confirmation_Authorize_for_Credit_Card from netbank where Cust_Id = {customer_id}"""
        smseva_output = sms_eva_Model.objects.raw(smseva_query)
        netbank_output = netbanking_Model.objects.raw(netbank_query)
        return render(request,'index.html',{"smseva":smseva_output,"netbank":netbank_output})
        #return render(request,'index.html',{"netbank":netbank_output})

    elif (request.method=="POST" and request.POST.get("choose-channel-select")=="smseva"):
        smseva_output = sms_eva_Model.objects.all()[:10]
        return render(request,'index.html',{"smseva":smseva_output})
    
    elif (request.method=="POST" and request.POST.get("choose-channel-select")=="netbanking"):
        netbank_output = netbanking_Model.objects.all()[:10]
        return render(request,'index.html',{"netbank":netbank_output})
    
    else:
        smseva_output = sms_eva_Model.objects.all()[:10]
        netbank_output = netbanking_Model.objects.all()[:10]
        #print("LOG SMS EVA", smseva_output) 
        return render(request,'index.html',{"smseva":smseva_output,"netbank":netbank_output})


def export_excel_smseva(request):

    #print("request check::::::",request.POST.get('Customer_ID'))
    #print("request type check:::::",type(data))
    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Smseva.xls"'
        
    wb = xlwt.Workbook(encoding='UTF-8')
    ws = wb.add_sheet('smseva')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['PseudoId', 'PcId', 'MobileNumber', 'Current_Category', 'Eligible_Category', 'Consent_Of_User', 'Consent_Time', 'CustomerName', 'Existing_Branch', 'Change_Branch', 'Change_Rm','Employee_Code', 'State', 'City', 'Branch', 'Branch_Code', 'Existing_Branch_Code', 'SessionID', 'IPAddress','Channel_Remarks', 'Device']
    
    #columns = ['Sr_No', 'Promo_code', 'Cust_Id' , 'Customer_Name','Eligible_Programme', 'Account_no', 'Home_BranchName' ,'Home_BranchCode','CR_programme_RM_Change' ,'Credit_Card', 'DC_Upgrade' ,'Selected_Branchname' ,'Selected_Branchcode','Employee_Code','Confirmation_authorize','IP_Address' ,'Session_Id' ,'User_Agent' ,'Lead_Date' ,'Confirmation_Authorize_for_Debit_Card' ,'Confirmation_Authorize_for_Credit_Card']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

       
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    
    customer_id= cust_id

    branch_code = branch_id


    rows = sms_eva_Model.objects.values_list('pseudoId', 'pcId', 'mobilenumber', 'current_category', 'eligible_category', 'consent_of_user', 'consent_time', 'CustomerName', 'existing_branch', 'change_branch', 'change_rm','employee_code', 'state', 'city', 'branch', 'branch_code', 'existing_branch_code', 'sessionID', 'IPaddress','channel_remarks', 'device').filter(Q(pcId__contains=customer_id)).filter(Q(branch_code__contains=branch_code) | Q(existing_branch_code__contains=branch_code))

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response






def export_excel_netbanking(request):
    #if request.POST.get('Branch_Code'):
    #    pass
    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="netbanking.xls"'
        
    wb = xlwt.Workbook(encoding='UTF-8')
    ws = wb.add_sheet('netbank')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    #columns = ['pseudoId', 'pcId', 'mobilenumber', 'current_category', 'eligible_category', 'consent_of_user', 'consent_time', 'CustomerName', 'existing_branch', 'change_branch', 'change_rm','employee_code', 'state', 'city', 'branch', 'branch_code', 'existing_branch_code', 'sessionID', 'IPaddress','channel_remarks', 'device']
    
    columns = ['Sr_No', 'Promo_Code', 'Cust_Id' , 'Customer_Name','Eligible_Programme', 'Account_No', 'Home_BranchName' ,'Home_BranchCode','CR_programme_RM_Change' ,'Credit_Card', 'DC_Upgrade' ,'Selected_Branchname' ,'Selected_Branchcode','Employee_Code','Confirmation_Authorize','IP_Address' ,'Session_Id' ,'User_Agent' ,'Lead_Date' ,'Confirmation_Authorize_For_Debit_Card' ,'Confirmation_Authorize_For_Credit_Card']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    customer_id= cust_id

    branch_code = branch_id
    
    #rows = sms_eva_Model.objects.values_list('pseudoId', 'pcId', 'mobilenumber', 'current_category', 'eligible_category', 'consent_of_user', 'consent_time', 'CustomerName', 'existing_branch', 'change_branch', 'change_rm','employee_code', 'state', 'city', 'branch', 'branch_code', 'existing_branch_code', 'sessionID', 'IPaddress','channel_remarks', 'device')
    rows = netbanking_Model.objects.values_list('Sr_No', 'Promo_code', 'Cust_Id' , 'Customer_Name','Eligible_Programme', 'Account_no', 'Home_BranchName' ,'Home_BranchCode','CR_programme_RM_Change' ,'Credit_Card', 'DC_Upgrade' ,'Selected_Branchname' ,'Selected_Branchcode','Employee_Code','Confirmation_authorize','IP_Address' ,'Session_Id' ,'User_Agent' ,'Lead_Date' ,'Confirmation_Authorize_for_Debit_Card' ,'Confirmation_Authorize_for_Credit_Card').filter(Q(Cust_Id__contains=customer_id)).filter(Q(Home_BranchCode__contains=branch_code) | Q(Selected_Branchcode__contains=branch_code))
    
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response
