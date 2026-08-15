"""
Day 2 - Data Cleaning

Cleans the raw AMFI datasets and writes cleaned versions to Data/Processed/:
  - nav_history_clean.csv       : NAV history, forward-filled to daily grain per fund
  - investor_transactions_clean.csv : validated investor transactions
  - scheme_performance_clean.csv    : validated scheme performance metrics
  - monthly_sip_inflows_clean.csv   : SIP inflows (yoy_growth_pct nulls for 2022 expected)

Also copies through, unchanged, the 6 files that needed no cleaning
(01_fund_master, 03_aum_by_fund_house, 05_category_inflows,
06_industry_folio_count, 09_portfolio_holdings, 10_benchmark_indices).
"""

import pandas as pd
import shutil

RAW_DIR = "Data/Raw"
PROCESSED_DIR = "Data/Processed"

CLEAN_AS_IS_FILES = [
    "01_fund_master.csv",
    "03_aum_by_fund_house.csv",
    "05_category_inflows.csv",
    "06_industry_folio_count.csv",
    "09_portfolio_holdings.csv",
    "10_benchmark_indices.csv",
]


def clean_nav_history():
    """Forward-fill each fund's NAV series to a continuous daily grain (no gaps)."""
    nav = pd.read_csv(f"{RAW_DIR}/02_nav_history.csv")
    nav["date"] = pd.to_datetime(nav["date"])
    nav = nav.sort_values(["amfi_code", "date"])

    filled_parts = []
    for code in nav["amfi_code"].unique():
        fund_data = nav[nav["amfi_code"] == code].copy()
        fund_data = fund_data.set_index("date")

        full_range = pd.date_range(fund_data.index.min(), fund_data.index.max(), freq="D")
        fund_data = fund_data.reindex(full_range)

        fund_data["nav"] = fund_data["nav"].ffill()
        fund_data["amfi_code"] = code
        fund_data.index.name = "date"

        filled_parts.append(fund_data.reset_index())

    nav_clean = pd.concat(filled_parts, ignore_index=True)
    nav_clean.to_csv(f"{PROCESSED_DIR}/nav_history_clean.csv", index=False)
    print(f"nav_history_clean saved: {nav_clean.shape[0]} rows")
    return nav_clean


def clean_investor_transactions():
    """Standardize transaction type / KYC status text and validate amounts."""
    txn = pd.read_csv(f"{RAW_DIR}/08_investor_transactions.csv")
    txn["transaction_date"] = pd.to_datetime(txn["transaction_date"])
    txn["transaction_type"] = txn["transaction_type"].str.strip().str.title()
    txn["kyc_status"] = txn["kyc_status"].str.strip().str.title()

    valid_types = ["Sip", "Lumpsum", "Redemption"]
    invalid_types = txn[~txn["transaction_type"].isin(valid_types)]
    invalid_amounts = txn[txn["amount_inr"] <= 0]

    if len(invalid_types) or len(invalid_amounts):
        print(f"Warning: {len(invalid_types)} invalid transaction types, "
              f"{len(invalid_amounts)} invalid amounts found")

    txn_clean = txn.copy()
    txn_clean.to_csv(f"{PROCESSED_DIR}/investor_transactions_clean.csv", index=False)
    print(f"investor_transactions_clean saved: {txn_clean.shape[0]} rows")
    return txn_clean


def clean_scheme_performance():
    """Validate return columns and expense ratio range, then save cleaned copy."""
    perf = pd.read_csv(f"{RAW_DIR}/07_scheme_performance.csv")

    return_cols = ["return_1yr_pct", "return_3yr_pct", "return_5yr_pct"]
    for col in return_cols:
        non_numeric = perf[col].apply(lambda x: not isinstance(x, (int, float))).sum()
        if non_numeric:
            print(f"Warning: {non_numeric} non-numeric values in {col}")

    expense_out_of_range = perf[(perf["expense_ratio_pct"] < 0.1) | (perf["expense_ratio_pct"] > 2.5)]
    if len(expense_out_of_range):
        print(f"Warning: {len(expense_out_of_range)} funds with expense ratio outside 0.1%-2.5% range")

    perf_clean = perf.copy()
    perf_clean.to_csv(f"{PROCESSED_DIR}/scheme_performance_clean.csv", index=False)
    print(f"scheme_performance_clean saved: {perf_clean.shape[0]} rows")
    return perf_clean


def clean_monthly_sip_inflows():
    """Clean monthly SIP inflows. yoy_growth_pct is expected to be null for the
    first 12 months (Jan-Dec 2022) since no prior-year data exists to compare against."""
    sip_inflows = pd.read_csv(f"{RAW_DIR}/04_monthly_sip_inflows.csv")
    sip_clean = sip_inflows.copy()
    sip_clean.to_csv(f"{PROCESSED_DIR}/monthly_sip_inflows_clean.csv", index=False)
    print(f"monthly_sip_inflows_clean saved: {sip_clean.shape[0]} rows "
          f"(yoy_growth_pct null for 2022 by design)")
    return sip_clean


def copy_clean_as_is_files():
    """Copy through the files that required no cleaning."""
    for filename in CLEAN_AS_IS_FILES:
        src = f"{RAW_DIR}/{filename}"
        dst = f"{PROCESSED_DIR}/{filename}"
        shutil.copy(src, dst)
    print(f"Copied {len(CLEAN_AS_IS_FILES)} clean-as-is files to {PROCESSED_DIR}/")


def main():
    clean_nav_history()
    clean_investor_transactions()
    clean_scheme_performance()
    clean_monthly_sip_inflows()
    copy_clean_as_is_files()


if __name__ == "__main__":
    main()