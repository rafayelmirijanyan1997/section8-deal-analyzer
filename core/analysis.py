from .hud_api import get_hud_rent
from .mortgage import monthly_mortgage, total_monthly_cost
from .config import INTEREST_RATE, LOAN_YEARS

def analyze_deal(row):
    price = row["price"]
    zip_code = str(row["zip"])

    hud_rent = get_hud_rent(zip_code)

    principal = price * (1 - 0.20)
    mortgage = monthly_mortgage(principal, INTEREST_RATE, LOAN_YEARS)

    total_cost = total_monthly_cost(mortgage)
    cashflow = hud_rent - total_cost

    return {
        "listing_price": price,
        "hud_2br_rent": hud_rent,
        "monthly_mortgage": round(mortgage, 2),
        "total_monthly_cost": round(total_cost, 2),
        "monthly_cashflow": round(cashflow, 2)
    }
