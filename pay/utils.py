import pandas as pd
from django.contrib import messages


def process_payroll_file(file):
    try:
        df = pd.read_excel(file)
        data = []
        for _, row in df.iterrows():
            employee_data = {
                "employee_id": row.get('Employee ID', 'Unknown'),
                "name": row.get('Name', 'Unknown'),
            }
            data.append({
                "employee": employee_data,
                "gross_salary": row.get('Gross Salary', 0),
            })
        return data
    except Exception as e:
        raise ValueError(f"Error processing file: {e}")


def calculate_payroll_data(employee, gross_salary):
    net_salary = 0
    sp = 0
    sm = 0
    shp = 0
    shm = 0
    tap = 0
    pagaminimale = 40000
    pagamax = 176416
    fasha1 = 50000
    fasha2 = 60000
    fasha3 = 200000

    if gross_salary<0:
        sp = "Paga bruto nuk mund te jete me e vogel se 0"
        sm = "Paga bruto nuk mund te jete me e vogel se 0"
        shp = "Paga bruto nuk mund te jete me e vogel se 0"
        shm = "Paga bruto nuk mund te jete me e vogel se 0"
        net_salary = "Paga bruto nuk mund te jete me e vogel se 0"
    elif gross_salary <= fasha1 and gross_salary>=0:
        sp = gross_salary * 0.15
        sm = gross_salary * 0.095
        pg_kontributeve = gross_salary
        tot_sig = sp + sm
        shp = gross_salary * 0.017
        shm = gross_salary *0.017
        net_salary = gross_salary - sm - shm
    elif gross_salary <= fasha2 and gross_salary > fasha1:
        sp = gross_salary * 0.15
        sm = gross_salary * 0.095
        pg_kontributeve = gross_salary
        tot_sig = sp + sm
        shp = gross_salary * 0.017
        shm = gross_salary *0.017
        tap = (gross_salary-35000) * 0.13
        net_salary = gross_salary - sm - shm - tap
    elif gross_salary > fasha2 and gross_salary <= pagamax:
        sp = gross_salary * 0.15
        sm = gross_salary * 0.095
        pg_kontributeve = gross_salary
        tot_sig = sp + sm
        shp = gross_salary * 0.017
        shm = gross_salary *0.017
        tap = (gross_salary-30000) * 0.13
        net_salary = gross_salary - sm - shm - tap
    elif gross_salary > pagamax and gross_salary <= fasha3:
        sp = pagamax * 0.15
        sm = pagamax * 0.095
        pg_kontributeve = pagamax
        tot_sig = sp + sm
        shp = gross_salary * 0.017
        shm = gross_salary *0.017
        tap = (gross_salary-30000) * 0.13
        net_salary = gross_salary - sm - shm - tap
    elif gross_salary > fasha3:
        sp = pagamax * 0.15
        sm = pagamax * 0.095
        pg_kontributeve = pagamax
        tot_sig = sp + sm
        shp = gross_salary * 0.017
        shm = gross_salary *0.017
        tap = (gross_salary-200000) * 0.23 + 22100
        net_salary = gross_salary - sm - shm - tap

    return {
        "employee": employee,
        "gross_salary": round(gross_salary, 0),
        "pg_kontributeve": round(pg_kontributeve, 0) if 'pg_kontributeve' in locals() else 0,
        "sp": round(sp, 0) if isinstance(sp, (int, float)) else sp,
        "sm": round(sm, 0) if isinstance(sm, (int, float)) else sm,
        "tot_sig": round(tot_sig, 0) if 'tot_sig' in locals() else 0,
        "shp": round(shp, 0) if isinstance(shp, (int, float)) else shp,
        "shm": round(shm, 0) if isinstance(shm, (int, float)) else shm,
        "tap": round(tap, 0) if isinstance(tap, (int, float)) else tap,
        "net_salary": round(net_salary, 0) if isinstance(net_salary, (int, float)) else net_salary,
    }

def process_payroll_neto(file):
    try:
        df = pd.read_excel(file)
        data = []
        for _, row in df.iterrows():
            employee_data = {
                "employee_id": row.get('Employee ID', 'Unknown'),
                "name": row.get('Name', 'Unknown'),
            }
            data.append({
                "employee": employee_data,
                "net_salary": row.get('Net Salary', 0),
            })
        return data
    except Exception as e:
        raise ValueError(f"Error processing file: {e}")
    
def calculate_payroll_net(employee, net_salary):
    gross_salary = 0
    sp = 0
    sm = 0
    shp = 0
    shm = 0
    tap = 0
    pagaminimale = 40000
    pagamax_net = 137623
    pagamax = 176416
    fasha1 = 44400
    fasha2 = 50030
    fasha3 = 157740

    if net_salary<0:
        sp = "Paga bruto nuk mund te jete me e vogel se 0"
        sm = "Paga bruto nuk mund te jete me e vogel se 0"
        shp = "Paga bruto nuk mund te jete me e vogel se 0"
        shm = "Paga bruto nuk mund te jete me e vogel se 0"
        net_salary = "Paga bruto nuk mund te jete me e vogel se 0"
    elif net_salary <= fasha1 and net_salary>=0:
        gross_salary = net_salary /0.888
        sp = gross_salary * 0.15
        sm = gross_salary * 0.095
        pg_kontributeve = gross_salary
        tot_sig = sp + sm
        shp = gross_salary * 0.017
        shm = gross_salary *0.017
        net_salary = net_salary
    elif net_salary <= fasha2 and net_salary > fasha1:
        gross_salary = (net_salary - 4550)/0.758
        sp = gross_salary * 0.15
        sm = gross_salary * 0.095
        pg_kontributeve = gross_salary
        tot_sig = sp + sm
        shp = gross_salary * 0.017
        shm = gross_salary *0.017
        tap = (gross_salary-35000) * 0.13
        net_salary = net_salary
    elif net_salary > fasha2 and net_salary <= pagamax_net:
        gross_salary = (net_salary - 3900)/0.758
        sp = gross_salary * 0.15
        sm = gross_salary * 0.095
        pg_kontributeve = gross_salary
        tot_sig = sp + sm
        shp = gross_salary * 0.017
        shm = gross_salary *0.017
        tap = (gross_salary-30000) * 0.13
        net_salary = net_salary
    elif net_salary > pagamax_net and net_salary <= fasha3:
        gross_salary = (net_salary + 12859.52)/0.853
        sp = pagamax * 0.15
        sm = pagamax * 0.095
        pg_kontributeve = pagamax
        tot_sig = sp + sm
        shp = gross_salary * 0.017
        shm = gross_salary *0.017
        tap = (gross_salary-30000) * 0.13
        net_salary = net_salary
    elif net_salary > fasha3:
        gross_salary = (net_salary - 7140.48)/0.753
        sp = pagamax * 0.15
        sm = pagamax * 0.095
        pg_kontributeve = pagamax
        tot_sig = sp + sm
        shp = gross_salary * 0.017
        shm = gross_salary *0.017
        tap = (gross_salary-200000) * 0.23 + 22100
        net_salary = net_salary

    return {
        "employee": employee,
        "gross_salary": round(gross_salary, 0),
        "pg_kontributeve": round(pg_kontributeve, 0) if 'pg_kontributeve' in locals() else 0,
        "sp": round(sp, 0) if isinstance(sp, (int, float)) else sp,
        "sm": round(sm, 0) if isinstance(sm, (int, float)) else sm,
        "tot_sig": round(tot_sig, 0) if 'tot_sig' in locals() else 0,
        "shp": round(shp, 0) if isinstance(shp, (int, float)) else shp,
        "shm": round(shm, 0) if isinstance(shm, (int, float)) else shm,
        "tap": round(tap, 0) if isinstance(tap, (int, float)) else tap,
        "net_salary": round(net_salary, 0) if isinstance(net_salary, (int, float)) else net_salary,
    }