"""
Live NAV Fetch

Fetches live/latest NAV history for 6 benchmark schemes from the mfapi.in
public API and saves each as a CSV in Data/Raw/ (nav_<scheme_name>.csv).
"""

import requests
import pandas as pd
import os

RAW_DIR = "Data/Raw"

SCHEMES = {
    "125497": "HDFC_Top_100_Direct",
    "119551": "SBI_Bluechip",
    "120503": "ICICI_Bluechip",
    "118632": "Nippon_Large_Cap",
    "119092": "Axis_Bluechip",
    "120841": "Kotak_Bluechip",
}


def fetch_nav(scheme_code):
    """Fetch NAV history JSON for a single scheme code from mfapi.in."""
    url = "https://api.mfapi.in/mf/" + scheme_code
    response = requests.get(url)
    data = response.json()
    return data


def save_nav_csv(scheme_code, scheme_name, data):
    """Convert the fetched NAV JSON to a DataFrame and save as CSV in RAW_DIR."""
    nav_records = data["data"]
    df = pd.DataFrame(nav_records)
    df["scheme_code"] = scheme_code
    df["scheme_name"] = scheme_name
    output_path = os.path.join(RAW_DIR, "nav_" + scheme_name + ".csv")
    df.to_csv(output_path, index=False)
    print("Saved:", output_path, "-", len(df), "rows")


def main():
    for code, name in SCHEMES.items():
        print("Fetching:", name, "(" + code + ")")
        data = fetch_nav(code)
        save_nav_csv(code, name, data)
    print("All live NAV data fetched and saved.")


if __name__ == "__main__":
    main()