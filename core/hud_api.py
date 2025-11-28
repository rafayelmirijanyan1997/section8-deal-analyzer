import requests
import os

HUD_API_BASE = "https://www.huduser.gov/hudapi/public"
HUD_FMR_ENDPOINT = f"{HUD_API_BASE}/fmr"  # adjust if you use SAFMR endpoint

HUD_API_KEY = os.getenv("HUD_API_KEY")

def get_fmr(zip_code: str, beds: int, year: int = 2025) -> float | None:
    """
    Return Fair Market Rent for given ZIP + bedroom count, or None if not found.
    """
    headers = {"apikey": HUD_API_KEY}
    params = {
        "zip_code": zip_code,
        "year": year
    }
    resp = requests.get(HUD_FMR_ENDPOINT, headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json()

    # HUD response format may differ; adjust this mapping based on the API docs.
    # Example shape:
    # { "data": [{ "ZipCode": "48127", "FMR2": 1350, "FMR3": 1700, ... }] }
    records = data.get("data", [])
    if not records:
        return None

    record = records[0]
    # Map bedroom count → field name
    field = f"FMR{beds}"
    return float(record.get(field)) if record.get(field) is not None else None
