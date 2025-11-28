import math

def monthly_payment(principal: float, annual_rate: float, years: int) -> float:
    r = annual_rate / 100 / 12
    n = years * 12
    if r == 0:
        return principal / n
    return principal * (r * (1 + r) ** n) / ((1 + r) ** n - 1)

def estimate_monthly_expenses(
    annual_tax: float,
    annual_insurance: float,
    hoa_monthly: float,
    maintenance_pct: float,
    management_pct: float,
    rent: float,
) -> float:
    """
    maintenance_pct and management_pct are percentages of rent (e.g. 10 for 10%).
    """
    monthly_tax = annual_tax / 12
    monthly_ins = annual_insurance / 12
    maintenance = rent * (maintenance_pct / 100)
    management = rent * (management_pct / 100)
    return monthly_tax + monthly_ins + hoa_monthly + maintenance + management
