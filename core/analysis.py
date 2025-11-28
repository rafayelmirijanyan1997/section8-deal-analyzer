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
import pandas as pd
from .hud_api import get_fmr
from .mortgage import monthly_payment, estimate_monthly_expenses

def analyze_properties(
    df: pd.DataFrame,
    hud_year: int,
    assumptions: dict,
):
    """
    df must have: price, bedrooms, state, zip, tax_annual, insurance_annual, hoa_monthly
    """
    rows = []
    for _, row in df.iterrows():
        price = float(row["price"])
        beds = int(row["bedrooms"])
        zip_code = str(row["zip"])
        state = row["state"]

        fmr = get_fmr(zip_code, beds, year=hud_year)
        if fmr is None:
            continue

        down_payment = price * assumptions["down_payment_pct"] / 100
        loan_amount = price - down_payment
        mortgage = monthly_payment(loan_amount,
                                   assumptions["interest_rate"],
                                   assumptions["loan_years"])

        monthly_expenses = estimate_monthly_expenses(
            annual_tax=row.get("tax_annual", 0.0),
            annual_insurance=row.get("insurance_annual", 0.0),
            hoa_monthly=row.get("hoa_monthly", 0.0),
            maintenance_pct=assumptions["maintenance_pct"],
            management_pct=assumptions["management_pct"],
            rent=fmr,
        )

        monthly_total_cost = mortgage + monthly_expenses
        monthly_cash_flow = fmr - monthly_total_cost
        annual_cash_flow = monthly_cash_flow * 12

        cash_in = down_payment + assumptions["closing_costs"] + row.get("repairs_estimate", 0.0)
        cash_on_cash = (annual_cash_flow / cash_in) * 100 if cash_in > 0 else None
        cap_rate = (fmr * 12 / price) * 100 if price > 0 else None

        rows.append({
            "address": row["address"],
            "city": row.get("city", ""),
            "state": state,
            "zip": zip_code,
            "price": price,
            "beds": beds,
            "fmr_rent": fmr,
            "mortgage": mortgage,
            "monthly_expenses": monthly_expenses,
            "monthly_total_cost": monthly_total_cost,
            "monthly_cash_flow": monthly_cash_flow,
            "annual_cash_flow": annual_cash_flow,
            "cash_on_cash": cash_on_cash,
            "cap_rate": cap_rate,
            "source_url": row.get("url", "")
        })

    return pd.DataFrame(rows)
