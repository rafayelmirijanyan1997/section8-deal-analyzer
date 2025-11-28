# core/analysis.py
import pandas as pd
from .hud_api import get_hud_rent       # ✅ name matches hud_api.py
from .mortgage import monthly_payment, estimate_monthly_expenses

def analyze_properties(
    df: pd.DataFrame,
    hud_year: int,
    assumptions: dict,
):
    rows = []
    for _, row in df.iterrows():
        price = float(row["price"])
        beds = int(row["bedrooms"])
        zip_code = str(row["zip"])
        state = row["state"]

        hud_rent = get_hud_rent(zip_code, beds, year=hud_year)
        if hud_rent is None:
            continue

        down_payment = price * assumptions["down_payment_pct"] / 100
        loan_amount = price - down_payment

        mortgage = monthly_payment(
            loan_amount,
            assumptions["interest_rate"],
            assumptions["loan_years"],
        )

        monthly_expenses = estimate_monthly_expenses(
            annual_tax=row.get("tax_annual", 0.0),
            annual_insurance=row.get("insurance_annual", 0.0),
            hoa_monthly=row.get("hoa_monthly", 0.0),
            maintenance_pct=assumptions["maintenance_pct"],
            management_pct=assumptions["management_pct"],
            rent=hud_rent,
        )

        monthly_total_cost = mortgage + monthly_expenses
        monthly_cash_flow = hud_rent - monthly_total_cost
        annual_cash_flow = monthly_cash_flow * 12

        cash_in = (
            down_payment
            + assumptions["closing_costs"]
            + row.get("repairs_estimate", 0.0)
        )
        cash_on_cash = (
            (annual_cash_flow / cash_in) * 100 if cash_in > 0 else None
        )
        cap_rate = (hud_rent * 12 / price) * 100 if price > 0 else None

        rows.append({
            "address": row["address"],
            "city": row.get("city", ""),
            "state": state,
            "zip": zip_code,
            "price": price,
            "beds": beds,
            "hud_rent": hud_rent,
            "mortgage": mortgage,
            "monthly_expenses": monthly_expenses,
            "monthly_total_cost": monthly_total_cost,
            "monthly_cash_flow": monthly_cash_flow,
            "annual_cash_flow": annual_cash_flow,
            "cash_on_cash": cash_on_cash,
            "cap_rate": cap_rate,
            "source_url": row.get("url", ""),
        })

    return pd.DataFrame(rows)
