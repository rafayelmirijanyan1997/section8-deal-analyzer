def monthly_mortgage(principal, interest_rate, years=30):
    r = interest_rate / 12
    n = years * 12
    payment = (principal * r * (1 + r)**n) / ((1 + r)**n - 1)
    return payment

def total_monthly_cost(mortgage, taxes=200, insurance=120, maintenance=150):
    return mortgage + taxes + insurance + maintenance