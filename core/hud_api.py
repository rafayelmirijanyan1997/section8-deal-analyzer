import requests
from .config import HUD_API_KEY

def get_hud_rent(zip_code: str):
    url = f"https://www.huduser.gov/hudapi/public/fmr?year=2024&zip={zip_code}"
    headers = {"Authorization": f"Bearer {HUD_API_KEY}"}

    r = requests.get(url, headers=headers)
    data = r.json()

    rent = data["data"][0]["rent50_2br"]
    return rent