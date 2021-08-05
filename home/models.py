from django.db import models

# Create your models here.
from django.db import models
from django.db.models.fields import CharField, IntegerField



class sms_eva_Model(models.Model):
    pseudoId = models.CharField(max_length=4000,primary_key='pseudoId')
    mobilenumber = models.IntegerField()
    current_category = models.CharField(max_length=4000)
    pcId = models.CharField(max_length=4000)
    eligible_category = models.CharField(max_length=4000)
    consent_of_user = models.CharField(max_length=4000)
    consent_time = models.CharField(max_length=4000)
    CustomerName = models.CharField(max_length=4000)
    sessionID = models.CharField(max_length=4000)
    IPaddress = models.CharField(max_length=4000)
    channel_remarks =models.CharField(max_length=4000)
    device  = models.CharField(max_length=4000)
    existing_branch = models.CharField(max_length=4000)
    change_branch = models.CharField(max_length=4000)
    change_rm = models.CharField(max_length=4000)
    employee_code = models.CharField(max_length=4000)
    state = models.CharField(max_length=4000)
    city = models.CharField(max_length=4000)
    branch = models.CharField(max_length=4000)
    branch_code = models.CharField(max_length=4000)
    existing_branch_code = models.IntegerField()

    class Meta:
        db_table="smseva"




class netbanking_Model(models.Model):
    Sr_No = models.IntegerField(primary_key='Sr_No')
    Promo_code = models.CharField(max_length=4000)
    Pseudo_Id =models.CharField(max_length=4000)
    Customer_Name = models.CharField(max_length=400)
    Eligible_Programme = models.CharField(max_length=4000)
    Account_no = models.IntegerField()
    Home_BranchName = models.CharField(max_length=4000)
    Home_BranchCode = models.IntegerField()
    CR_programme_RM_Change = models.CharField(max_length=4000)
    Credit_Card = models.CharField(max_length=4000)
    DC_Upgrade = models.CharField(max_length=4000)
    Selected_Branchname = models.CharField(max_length=4000)
    Selected_Branchcode = models.IntegerField()
    Employee_Code = models.CharField(max_length=4000)
    Confirmation_authorize = models.CharField(max_length=4000)
    IP_Address = models.CharField(max_length=4000)
    Session_Id = models.CharField(max_length=4000)
    User_Agent = models.CharField(max_length=4000)
    Lead_Date = models.CharField(max_length=4000)
    Confirmation_Authorize_for_Debit_Card  = models.CharField(max_length=4000)
    Confirmation_Authorize_for_Credit_Card = models.CharField(max_length=4000)
    class Meta:
        db_table="netbank"



