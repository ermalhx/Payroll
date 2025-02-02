from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import PayrollUploadForm
from .utils import *
from django.http import HttpResponse
import pandas as pd
# Create your views here.

def upload_payroll_preview(request):
    calculated_data = []
    if request.method == 'POST':
        form = PayrollUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                file = form.cleaned_data['file']
                payroll_data = process_payroll_file(file)
                for entry in payroll_data:
                    details = calculate_payroll_data(
                        employee=entry["employee"],
                        gross_salary=entry["gross_salary"]
                    )
                    calculated_data.append(details)
                request.session['calculated_data'] = calculated_data
            except Exception as e:
                messages.error(request, f"Error: {e}")
    else:
        form = PayrollUploadForm()
    return render(request, 'dashboard.html', {'form': form, 'calculated_data': calculated_data})

def download_payroll_excel(request):
    # Simulate payroll data (replace this with the actual data you want to download)
    calculated_data = request.session.get('calculated_data', [])  # Retrieve from session
    
    if not calculated_data:
        return HttpResponse("No payroll data to download.", status=400)

    # Prepare the data for Excel
    data = []
    for entry in calculated_data:
        data.append({
            "Kodi i punjesit": entry["employee"]["employee_id"],
            "Emer Mbiemer": entry["employee"]["name"],
            "Paga bruto": entry["gross_salary"],
            "Paga per kontribute": entry["pg_kontributeve"],
            "Sig Shoq Punedhenes": entry["sp"],
            "Sig Shoq Punemarres": entry["sm"],
            "Total Sigurime Shoq": entry["tot_sig"],
            "Sig Shend Punedhenes": entry["shp"],
            "Sig Shend Punemarres": entry["shm"],
            "TAP": entry["tap"],
            "Paga neto": entry["net_salary"],
        })
    
    # Create a DataFrame
    df = pd.DataFrame(data)
    
    # Generate Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="payroll_data.xlsx"'
    
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Payroll')
    
    return response

def upload_payroll_neto(request):
    calculated_data_neto = []
    if request.method == 'POST':
        form = PayrollUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                file = form.cleaned_data['file']
                payroll_data = process_payroll_neto(file)
                for entry in payroll_data:
                    details = calculate_payroll_net(
                        employee=entry["employee"],
                        net_salary=entry["net_salary"]
                    )
                    calculated_data_neto.append(details)
                request.session['calculated_data_neto'] = calculated_data_neto
            except Exception as e:
                messages.error(request, f"Error: {e}")
    else:
        form = PayrollUploadForm()
    return render(request, 'neto.html', {'form': form, 'calculated_data_neto': calculated_data_neto})

def download_payroll_excel_neto(request):
    # Simulate payroll data (replace this with the actual data you want to download)
    calculated_data_neto = request.session.get('calculated_data_neto', [])  # Retrieve from session
    
    if not calculated_data_neto:
        return HttpResponse("No payroll data to download.", status=400)

    # Prepare the data for Excel
    data = []
    for entry in calculated_data_neto:
        data.append({
            "Kodi i punjesit": entry["employee"]["employee_id"],
            "Emer Mbiemer": entry["employee"]["name"],
            "Paga bruto": entry["gross_salary"],
            "Paga per kontribute": entry["pg_kontributeve"],
            "Sig Shoq Punedhenes": entry["sp"],
            "Sig Shoq Punemarres": entry["sm"],
            "Total Sigurime Shoq": entry["tot_sig"],
            "Sig Shend Punedhenes": entry["shp"],
            "Sig Shend Punemarres": entry["shm"],
            "TAP": entry["tap"],
            "Paga neto": entry["net_salary"],
        })
    
    # Create a DataFrame
    df = pd.DataFrame(data)
    
    # Generate Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="payroll_data.xlsx"'
    
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Payroll')
    
    return response

def download_excel_template_bruto(request):
    # Define the template structure
    template_data = {
        "Employee ID": [""],  # Leave it empty for the template
        "Name": [""],
        "Gross Salary": [""],
    }

    # Create a DataFrame
    df = pd.DataFrame(template_data)

    # Generate an Excel response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="payroll_template.xlsx"'

    # Write the DataFrame to the response using openpyxl
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Template')

    return response
def download_excel_template_neto(request):
    # Define the template structure
    template_data = {
        "Employee ID": [""],  # Leave it empty for the template
        "Name": [""],
        "Net Salary": [""],
    }

    # Create a DataFrame
    df = pd.DataFrame(template_data)

    # Generate an Excel response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="payroll_template.xlsx"'

    # Write the DataFrame to the response using openpyxl
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Template')

    return response