from django.urls import path
from.import views

urlpatterns = [
    path('consentRepo', views.index, name='index'),
    path('',views.smseva,name='export_excel_smseva'),
    path('export/excel/smseva/',views.export_excel_smseva,name='export_excel_smseva'),
    path('export/excel/netbanking/',views.export_excel_netbanking,name='export_excel_netbanking'),
]
