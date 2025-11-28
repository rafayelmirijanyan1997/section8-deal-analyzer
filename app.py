import streamlit as st
import pandas as pd
from core.analysis import analyze_deal
from core.config import HUD_ZIP_RENT_FILE

st.title("🏘️ Section 8 Deal Analyzer")

uploaded = st.file_uploader("Upload Zillow/InvestorLift CSV", type=["csv"])

if uploaded:
    df = pd.read_csv(uploaded)
    st.write(df.head())

    selected_row = st.selectbox(
        "Select a property to analyze",
        df.index,
        format_func=lambda i: f"{df.loc[i, 'address']} - ${df.loc[i, 'price']}"
    )

    if st.button("Analyze Deal"):
        result = analyze_deal(df.loc[selected_row])
        st.write("### Deal Analysis Result:")
        st.json(result)
else:
    st.info("Upload a Zillow or InvestorLift CSV to begin.")
