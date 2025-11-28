# core/hud_api.py
import os
import requests

HUD_API_BASE = "https://www.huduser.gov/hudapi/public"
HUD_FMR_ENDPOINT = f"{HUD_API_BASE}/fmr"

HUD_API_KEY = os.getenv("HUD_API_KEY")

def get_hud_rent(zip_code: str, beds: int, year: int = 2025) -> float | None:
    """
    Return HUD Fair Market Rent (FMR) for a given ZIP + bedroom count.
    Adjust JSON parsing based on actual API response.
    """
    if HUD_API_KEY is None:
        # For first testing, you can return a fake constant value
        # so the rest of the app works.
        return 1200.0

    headers = {"apikey": HUD_API_KEY}
    params = {
        "zip_code": zip_code,
        "year": year,
    }
    resp = requests.get(HUD_FMR_ENDPOINT, headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json()

    # Adjust this according to actual HUD response structure
    records = data.get("data", [])
    if not records:
        return None

    record = records[0]
    field = f"FMR{beds}"
    value = record.get(field)
    return float(value) if value is not None else None
