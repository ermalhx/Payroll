from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import *
from .utils import *
from django.http import HttpResponse
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from io import BytesIO
from django.forms import formset_factory
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

def generate_payslip_pdf(request, employee_id):
    calculated_data = request.session.get('calculated_data', [])
    
    # Find the specific employee's payslip
    payslip_data = next((entry for entry in calculated_data if str(entry["employee"]["employee_id"]) == str(employee_id)), None)
    
    if not payslip_data:
        return HttpResponse("Payslip not found", status=404)
    
    # Create PDF in memory
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    pdf.setTitle(f"Payslip_{employee_id}.pdf")
    width, height = A4

    # Add Payslip Details
'''
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(120, height - 50, "EVIDENCA PËR ELEMENTET E PAGËS SË PUNONJËSIT")

    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, height - 70, "Në zbatim të nenit 118 pika 1.1 e ligjit nr.136/2015 ku përcaktohet se:Punëdhënësi vë në dispozicion")
    pdf.drawString(50, height - 80, "të punëmarrësit, në mënyrë periodike, me mënyra dhe mjete të vërtetueshme,përpara ose menjëherë")
    pdf.drawString(50, height - 90, "pas ekzekutimit të pagës, evidencë për të gjitha elementet e pagës, shtesat e përfituara dhe ndalimet")
    pdf.drawString(50, height - 100, "e mbajtura, sipas legjislacionit në fuqi.")

    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(50, height - 130, "Emri i Subjektit:")
    pdf.drawString(150, height - 130, "XXXZZZZCVVVVVV")
    pdf.drawString(400, height - 130, "NIPT: XXXXXXXXX")

    pdf.drawString(50, height - 150, "Lloji i Aktivitetit:")
    pdf.drawString(150, height - 150, "YYYyyyyyyyyyyyyyyyyyyyy")
    pdf.drawString(400, height - 150, "Periudha: Dhjetor 2024")

    pdf.drawString(50, height - 170, "Emri dhe Mbiemri i Punëmarrësit:")
    pdf.drawString(215, height - 170, payslip_data['employee']['name'])
    pdf.drawString(50, height - 190, "Pozicioni i Punës: YYYYYYYYYYYYYYYYY")

    pdf.drawString(50, height - 210, "Datëlindja:")
    pdf.drawString(150, height - 210, "7/27/1990")  # Replace with actual date
    pdf.drawString(50, height - 230, "Nr. I Sig. Shoq.: XXXXXXXXYYY")

    pdf.drawString(50, height - 250, "Data e Punësimit:")
    pdf.drawString(150, height - 250, "11/2/2020")

    pdf.setFont("Helvetica", 10)
    y_position = height - 280
    elements = [
        ("PAGA BRUTO", payslip_data['gross_salary']),
        ("1) Gjithsej (Paga bazë)", payslip_data['gross_salary']),
        ("Baza për llogaritje, kontribute shtesë", 0),
        ("2) Mbi të cilën llogariten kontributet", payslip_data['pg_kontributeve']),
        ("Kontribute për sigurimet shoqërore", payslip_data['tot_sig']),
        ("   4) Punëdhënësi", payslip_data['sp']),
        ("   5) Punëmarrësi", payslip_data['sm']),
        ("Kontribute për sigurimet shëndetësore", payslip_data['tot_sig']),
        ("   8) Punëdhënësi", payslip_data['shp']),
        ("   9) Punëmarrësi", payslip_data['shm']),
        ("10) Paga bruto mbi të cilën llogaritet Tatimi mbi të ardhurat", payslip_data['gross_salary']),
        ("11) Tatimi mbi të ardhurat nga punësimi", payslip_data['tap']),
        ("12) PAGA NETO = (1-5-9-11)", payslip_data['net_salary']),
    ]

    for label, value in elements:
        pdf.drawString(50, y_position, label)
        pdf.drawRightString(550, y_position, f"{value:,.2f} ALL")
        y_position -= 20

    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(50, y_position - 30, f"Punëmarrësi: {payslip_data['employee']['name']}")
    pdf.drawString(50, y_position - 50, "Data: 12/28/2024")
    pdf.drawString(50, y_position - 70, "Nënshkrimi: ___________________")

    pdf.save()

    # Prepare response
    buffer.seek(0)
    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Payslip_{employee_id}.pdf"'
    
    return response
'''
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

def salary_calculator_view(request):
    PagaFormSet = formset_factory(PagaForm, extra=1)  # Allow formset expansion
    jobs = []
    total_net_salary = 0

    if request.method == 'POST':
        formset = PagaFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                gross_salary = form.cleaned_data.get('gross_salary')
                deklarata = form.cleaned_data.get('deklarata', False)

                # Initialize net_salary before calculations
                net_salary = 0

                if gross_salary < 0:
                    messages.error(request, "Paga bruto nuk mund te jete me e vogel se 0")
                elif deklarata:
                    payroll_data = calculate_payroll_Bruto(gross_salary)
                    if isinstance(payroll_data["net_salary"], str):  # Check if error message is returned
                        messages.error(request, payroll_data["net_salary"])
                    else:
                        net_salary = payroll_data["net_salary"]
                        jobs.append({
                            'gross_salary': payroll_data["gross_salary"],
                            'pg_kontributeve': payroll_data["pg_kontributeve"],
                            'sp': payroll_data["sp"],
                            'sm': payroll_data["sm"],
                            'tot_sig': payroll_data["tot_sig"],
                            'shp': payroll_data["shp"],
                            'shm': payroll_data["shm"],
                            'tap': payroll_data["tap"],
                            'net_salary': net_salary
                        })
                else:
                    payroll_data = calculate_payroll_Pa_Deklarate(gross_salary)
                    if isinstance(payroll_data["net_salary"], str):  # Check if error message is returned
                        messages.error(request, payroll_data["net_salary"])
                    else:
                        net_salary = payroll_data["net_salary"]
                        jobs.append({
                            'gross_salary': payroll_data["gross_salary"],
                            'pg_kontributeve': payroll_data["pg_kontributeve"],
                            'sp': payroll_data["sp"],
                            'sm': payroll_data["sm"],
                            'tot_sig': payroll_data["tot_sig"],
                            'shp': payroll_data["shp"],
                            'shm': payroll_data["shm"],
                            'tap': payroll_data["tap"],
                            'net_salary': net_salary
                        })

                # Only add to total if net_salary is valid (int/float)
                if isinstance(net_salary, (int, float)):
                    total_net_salary += net_salary
        else:
            messages.error(request, "Formulari nuk eshte valid.")

    else:
        formset = PagaFormSet()

    return render(request, 'newcalc.html', {'formset': formset, 'jobs': jobs, 'total_net_salary': total_net_salary})
