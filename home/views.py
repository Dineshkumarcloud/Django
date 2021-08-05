##### Import Packages ######
from django.core import paginator
from django.shortcuts import render
from django.http import HttpResponse, request, response
from datetime import date, datetime
from django.utils.encoding import smart_bytes
from home.models import sms_eva_Model
from home.models import netbanking_Model
import xlwt
import json
from io import BytesIO as IO
from django.core.paginator import Paginator
from django.http import StreamingHttpResponse
from django.db.models import Q
import dateutil.parser
from django.utils.dateformat import DateFormat
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
    global cust_id,branch_id
    
    cust_id = request.POST.get('Customer_ID')
    branch_id = request.POST.get('Branch_Code')


    if (request.method =="POST" and request.POST.get('Branch_Code')):
        #global branch_code
        branch_code = request.POST.get('Branch_Code')
        
        smseva_query =f"""select pseudoId, mobilenumber, current_category,pcId,eligible_category, consent_of_user, consent_time, CustomerName, sessionID, IPaddress, channel_remarks, device,existing_branch, change_branch, change_rm, employee_code, state, city, branch, branch_code, existing_branch_code from smseva where convert(varchar,branch_code) = '{branch_code}' or convert(varchar,existing_branch_code) = '{branch_code}'"""
        netbank_query=f"""select Sr_No,Promo_code, Pseudo_Id ,Customer_Name ,Eligible_Programme ,Account_no, Home_BranchName ,Home_BranchCode, CR_programme_RM_Change,Credit_Card ,DC_Upgrade ,Selected_Branchname, Selected_Branchcode, Employee_Code,Confirmation_authorize ,IP_Address ,Session_Id ,User_Agent, Lead_Date ,Confirmation_Authorize_for_Debit_Card, Confirmation_Authorize_for_Credit_Card from netbank where convert(varchar,Home_BranchCode) = '{branch_code}' or convert(varchar,Selected_Branchcode) = '{branch_code}'"""
        
        smseva_output = sms_eva_Model.objects.raw(smseva_query)
        netbank_output = netbanking_Model.objects.raw(netbank_query)        
        return render(request,'index.html',{"smseva":smseva_output,"netbank":netbank_output})

    
    elif (request.method =="POST" and request.POST.get('fromdate') and  request.POST.get('todate')):
        #global fromdate,todate
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        print("test from_date",fromdate,todate)
        smseva_query =f"""select pseudoId, mobilenumber, current_category,pcId,eligible_category, consent_of_user, consent_time, CustomerName, sessionID, IPaddress, channel_remarks, device,existing_branch, change_branch, change_rm, employee_code, state, city, branch, branch_code, existing_branch_code from smseva where convert(date,consent_time)  between '{fromdate}'  and '{todate}' """
        netbank_query=f"""select Sr_No,Promo_code, Pseudo_Id ,Customer_Name ,Eligible_Programme ,Account_no, Home_BranchName ,Home_BranchCode, CR_programme_RM_Change,Credit_Card ,DC_Upgrade ,Selected_Branchname, Selected_Branchcode, Employee_Code,Confirmation_authorize ,IP_Address ,Session_Id ,User_Agent, Lead_Date ,Confirmation_Authorize_for_Debit_Card, Confirmation_Authorize_for_Credit_Card from netbank where convert(date,Lead_Date)  between '{fromdate}' and '{todate}' """
        smseva_output = sms_eva_Model.objects.raw(smseva_query)
        netbank_output = netbanking_Model.objects.raw(netbank_query)
        return render(request,'index.html',{"smseva":smseva_output,"netbank":netbank_output})


    elif (request.method =="POST" and request.POST.get('Customer_ID')):

        customer_id = request.POST.get('Customer_ID')
        print("customer_id_check::::",customer_id)
        smseva_query =f"""select pseudoId, mobilenumber, current_category,pcId,eligible_category, consent_of_user, consent_time, CustomerName, sessionID, IPaddress, channel_remarks, device,existing_branch, change_branch, change_rm, employee_code, state, city, branch, branch_code, existing_branch_code from smseva where pseudoId = '{customer_id}' """
        netbank_query=f"""select Sr_No,Promo_code, Pseudo_Id ,Customer_Name ,Eligible_Programme ,Account_no, Home_BranchName ,Home_BranchCode, CR_programme_RM_Change,Credit_Card ,DC_Upgrade ,Selected_Branchname, Selected_Branchcode, Employee_Code,Confirmation_authorize ,IP_Address ,Session_Id ,User_Agent, Lead_Date ,Confirmation_Authorize_for_Debit_Card, Confirmation_Authorize_for_Credit_Card from netbank where Pseudo_Id = '{customer_id}' """
        smseva_output = sms_eva_Model.objects.raw(smseva_query)
        netbank_output = netbanking_Model.objects.raw(netbank_query)
        return render(request,'index.html',{"smseva":smseva_output,"netbank":netbank_output})

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
    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Smseva_"'+str(datetime.now())+'.xls'
        
    wb = xlwt.Workbook(encoding='UTF-8')
    ws = wb.add_sheet('smseva')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['PseudoId', 'MobileNumber','Current_Category','PcId','Eligible_Category', 'Consent_Of_User', 'Consent_Time', 'CustomerName', 'SessionID','IPAddress','Channel_Remarks', 'Device','Existing_Branch', 'Change_Branch', 'Change_Rm','Employee_Code','State','City', 'Branch', 'Branch_Code', 'Existing_Branch_Code']


    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    customer_id= cust_id

    branch_code = branch_id
    

    rows = sms_eva_Model.objects.values_list('pseudoId', 'mobilenumber','current_category','pcId','eligible_category', 'consent_of_user', 'consent_time', 'CustomerName', 'sessionID','IPaddress','channel_remarks', 'device','existing_branch', 'change_branch', 'change_rm','employee_code','state','city', 'branch', 'branch_code', 'existing_branch_code').filter(Q(pseudoId__contains =customer_id)).filter(Q(branch_code__contains=branch_code) | Q(existing_branch_code__contains=branch_code))

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response



def export_excel_netbanking(request):

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="netbanking_"'+str(datetime.now())+'.xls'
        
    wb = xlwt.Workbook(encoding='UTF-8')
    ws = wb.add_sheet('netbank')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True


    columns = ['Sr_No', 'Promo_Code', 'Pseudo_Id' , 'Customer_Name','Eligible_Programme', 'Account_No', 'Home_BranchName' ,'Home_BranchCode','CR_programme_RM_Change' ,'Credit_Card', 'DC_Upgrade' ,'Selected_Branchname' ,'Selected_Branchcode','Employee_Code','Confirmation_Authorize','IP_Address' ,'Session_Id' ,'User_Agent' ,'Lead_Date' ,'Confirmation_Authorize_For_Debit_Card' ,'Confirmation_Authorize_For_Credit_Card']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    customer_id= cust_id

    branch_code = branch_id
    
    rows = netbanking_Model.objects.values_list('Sr_No', 'Promo_code', 'Pseudo_Id' , 'Customer_Name','Eligible_Programme', 'Account_no', 'Home_BranchName' ,'Home_BranchCode','CR_programme_RM_Change' ,'Credit_Card', 'DC_Upgrade' ,'Selected_Branchname' ,'Selected_Branchcode','Employee_Code','Confirmation_authorize','IP_Address' ,'Session_Id' ,'User_Agent' ,'Lead_Date' ,'Confirmation_Authorize_for_Debit_Card' ,'Confirmation_Authorize_for_Credit_Card').filter(Q(Pseudo_Id__contains=customer_id)).filter(Q(Home_BranchCode__contains=branch_code) | Q(Selected_Branchcode__contains=branch_code))

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response
