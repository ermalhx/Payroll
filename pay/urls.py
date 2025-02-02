from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
   path('', views.upload_payroll_preview, name='bruto'),
   path('download-payroll-excel/', views.download_payroll_excel, name='download_payroll_excel_bruto'),
   path('neto/', views.upload_payroll_neto, name='neto'),
   path('download-payroll-excel_neto/', views.download_payroll_excel_neto, name='download_payroll_excel'),
   path('download-template-bruto/', views.download_excel_template_bruto, name='download_template_bruto'),
   path('download-template-neto/', views.download_excel_template_neto, name='download_template_neto'),
]