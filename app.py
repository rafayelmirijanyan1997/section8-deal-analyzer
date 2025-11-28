import streamlit as st
import pandas as pd
from core.analysis import analyze_properties

st.set_page_config(page_title="Section 8 Deal Analyzer", layout="wide")

st.title("Section 8 Deal Analyzer 🏠")

# Sidebar: upload + assumptions
st.sidebar.header("Input & Assumptions")

uploaded_file = st.sidebar.file_uploader("Upload listings CSV", type=["csv"])
hud_year = st.sidebar.number_input("HUD Year", min_value=2020, max_value=2030, value=2025)

st.sidebar.subheader("Financing")
down_payment_pct = st.sidebar.slider("Down payment (%)", 0.0, 50.0, 20.0, 1.0)
interest_rate = st.sidebar.slider("Interest rate (%)", 0.0, 15.0, 6.5, 0.1)
loan_years = st.sidebar.selectbox("Loan term (years)", [15, 20, 25, 30], index=3)

st.sidebar.subheader("Expenses")
closing_costs = st.sidebar.number_input("Closing costs ($)", value=5000.0, step=1000.0)
maintenance_pct = st.sidebar.slider("Maintenance (% of rent)", 0.0, 20.0, 8.0, 0.5)
management_pct = st.sidebar.slider("Property management (% of rent)", 0.0, 20.0, 10.0, 0.5)

st.sidebar.subheader("Filters")
max_price = st.sidebar.number_input("Max price ($)", value=100000)
min_beds = st.sidebar.number_input("Min bedrooms", min_value=1, max_value=10, value=2)
target_states = st.sidebar.text_input("Target states (comma-separated, e.g. OH,MI,IN)", value="OH,MI,IN")

if uploaded_file is not None:
    raw_df = pd.read_csv(uploaded_file)

    # Filter before analysis to reduce HUD calls
    state_list = [s.strip().upper() for s in target_states.split(",") if s.strip()]
    filtered_df = raw_df[
        (raw_df["price"] <= max_price) &
        (raw_df["bedrooms"] >= min_beds) &
        (raw_df["state"].str.upper().isin(state_list))
    ]

    st.write(f"Loaded {len(raw_df)} listings, {len(filtered_df)} after filters.")

    if st.button("Run Analysis"):
        assumptions = {
            "down_payment_pct": down_payment_pct,
            "interest_rate": interest_rate,
            "loan_years": loan_years,
            "closing_costs": closing_costs,
            "maintenance_pct": maintenance_pct,
            "management_pct": management_pct,
        }

        result_df = analyze_properties(filtered_df, hud_year, assumptions)

        if result_df.empty:
            st.warning("No deals analyzed — check filters or HUD results.")
        else:
            # Sort by best monthly cash flow
            result_df = result_df.sort_values(by="monthly_cash_flow", ascending=False)

            st.subheader("Top Deals")
            st.dataframe(
                result_df[[
                    "address", "city", "state", "zip", "price",
                    "beds", "fmr_rent", "monthly_cash_flow",
                    "cash_on_cash", "cap_rate"
                ]]
            )

            # Detail view: select a property
            st.subheader("Deal Details")
            options = result_df["address"].tolist()
            selected_address = st.selectbox("Select a property", options)

            selected_row = result_df[result_df["address"] == selected_address].iloc[0]
            st.write(selected_row.to_frame().rename(columns={0: "Value"}))
else:
    st.info("Upload a CSV with columns: address, city, state, zip, price, bedrooms, tax_annual, insurance_annual, hoa_monthly, repairs_estimate, url.")
