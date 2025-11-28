# section8-deal-analyzer


# 🏘️ Section 8 Deal Analyzer

A small Streamlit app that helps you quickly analyze potential Section 8 rental deals by combining:

- Listing data (Zillow / InvestorLift exports)
- HUD Fair Market Rent (FMR) by ZIP
- Mortgage + operating cost assumptions

The goal is to make it fast and simple to answer:

> “If I buy this property and rent it with Section 8, will I have positive monthly cash flow?”

---

## 🚀 Features (MVP)

- Upload **Zillow / InvestorLift CSV** listings
- Filter deals by:
  - Price (e.g., under \$100k)
  - Min. number of bedrooms (e.g., 2+)
  - Section 8–friendly states
- Look up **HUD Fair Market Rent**:
  - Either via HUD API, or
  - From a pre-downloaded HUD ZIP rent CSV
- Run **deal analysis** per property:
  - Estimated Section 8 rent (from HUD)
  - Monthly mortgage payment
  - Estimated total monthly costs
  - Monthly cash flow

---

## 📁 Project Structure

```bash
section8-deal-analyzer/
├─ app.py                 # Streamlit app (UI + orchestration)
├─ core/
│   ├─ hud_api.py         # HUD API + CSV rent lookup
│   ├─ hud_parser.py      # (Optional) parse raw HUD CSV into clean ZIP rent file
│   ├─ mortgage.py        # Mortgage + expense calculations
│   ├─ analysis.py        # Combines listing + HUD rent + mortgage
│   ├─ sources.py         # Zillow / InvestorLift CSV / integration
│   └─ config.py          # HUD API keys, defaults, Section 8 states, etc.
├─ data/
│   ├─ listings.csv       # Example listing data (Zillow/InvestorLift export)
│   └─ hud_rent_by_zip.csv# Parsed HUD rent table (optional, generated)
├─ requirements.txt
└─ README.md




git clone https://github.com/<rafayelmirijanyan1997>/section8-deal-analyzer.git
cd section8-deal-analyzer

# (Optional) create venv
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate

pip install -r requirements.txt



streamlit run app.py