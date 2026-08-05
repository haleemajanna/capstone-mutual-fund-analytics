import pandas as pd

nav = pd.read_csv("Data/Raw/02_nav_history.csv")

print("Shape:", nav.shape)
print("\nData types:\n", nav.dtypes)
print("\nMissing values:\n", nav.isnull().sum())
print("\nDuplicate rows:", nav.duplicated().sum())
print("\nNAV values <= 0:", (nav["nav"] <= 0).sum())
print("\nFirst 5 rows:\n", nav.head())
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
print("\nCleaned shape:", nav_clean.shape)
print("\nRemaining missing values:\n", nav_clean.isnull().sum())
print("\nFirst 10 rows for one fund:\n", nav_clean[nav_clean["amfi_code"] == 119551].head(10))
nav_clean.to_csv("Data/Processed/nav_history_clean.csv", index=False)
print("\nSaved cleaned nav_history to Data/Processed/nav_history_clean.csv")

print("\n" + "="*50)
print("INVESTOR TRANSACTIONS")
print("="*50)

txn = pd.read_csv("Data/Raw/08_investor_transactions.csv")

print("Shape:", txn.shape)
print("\nData types:\n", txn.dtypes)
print("\nMissing values:\n", txn.isnull().sum())
print("\nFirst 5 rows:\n", txn.head())

print("\nUnique transaction_type values:", txn["transaction_type"].unique())
print("\nUnique kyc_status values:", txn["kyc_status"].unique())
print("\nUnique payment_mode values:", txn["payment_mode"].unique())
print("\nAmount <= 0 count:", (txn["amount_inr"] <= 0).sum())
print("\nMin amount:", txn["amount_inr"].min())
print("Max amount:", txn["amount_inr"].max())

txn["transaction_date"] = pd.to_datetime(txn["transaction_date"])
txn["transaction_type"] = txn["transaction_type"].str.strip().str.title()
txn["kyc_status"] = txn["kyc_status"].str.strip().str.title()

valid_types = ["Sip", "Lumpsum", "Redemption"]
invalid_types = txn[~txn["transaction_type"].isin(valid_types)]
print("\nRows with invalid transaction_type:", len(invalid_types))

invalid_amounts = txn[txn["amount_inr"] <= 0]
print("Rows with invalid amount:", len(invalid_amounts))

txn_clean = txn.copy()
txn_clean.to_csv("Data/Processed/investor_transactions_clean.csv", index=False)
print("\nSaved cleaned investor_transactions to Data/Processed/investor_transactions_clean.csv")

print("\n" + "="*50)
print("SCHEME PERFORMANCE")
print("="*50)

perf = pd.read_csv("Data/Raw/07_scheme_performance.csv")

print("Shape:", perf.shape)
print("\nData types:\n", perf.dtypes)
print("\nMissing values:\n", perf.isnull().sum())
print("\nFirst 5 rows:\n", perf.head())
print("\nColumn names:", list(perf.columns))

return_cols = ["return_1yr_pct", "return_3yr_pct", "return_5yr_pct"]
for col in return_cols:
    non_numeric = perf[col].apply(lambda x: not isinstance(x, (int, float))).sum()
    print(f"\nNon-numeric values in {col}: {non_numeric}")

expense_out_of_range = perf[(perf["expense_ratio_pct"] < 0.1) | (perf["expense_ratio_pct"] > 2.5)]
print("\nExpense ratio outside 0.1%-2.5% range:", len(expense_out_of_range))
if len(expense_out_of_range) > 0:
    print(expense_out_of_range[["scheme_name", "expense_ratio_pct"]])

perf_clean = perf.copy()
perf_clean.to_csv("Data/Processed/scheme_performance_clean.csv", index=False)
print("\nSaved cleaned scheme_performance to Data/Processed/scheme_performance_clean.csv")


print("\n" + "="*50)
print("QUICK CHECK: REMAINING 7 FILES")
print("="*50)

remaining_files = [
    "01_fund_master.csv",
    "03_aum_by_fund_house.csv",
    "04_monthly_sip_inflows.csv",
    "05_category_inflows.csv",
    "06_industry_folio_count.csv",
    "09_portfolio_holdings.csv",
    "10_benchmark_indices.csv",
]

for filename in remaining_files:
    df = pd.read_csv("Data/Raw/" + filename)
    missing = df.isnull().sum().sum()
    duplicates = df.duplicated().sum()
    print(f"\n{filename}: shape={df.shape}, missing_values={missing}, duplicate_rows={duplicates}")

    print("\n" + "="*50)
print("MONTHLY SIP INFLOWS - DETAILED CHECK")
print("="*50)

sip_inflows = pd.read_csv("Data/Raw/04_monthly_sip_inflows.csv")
print("\nColumns:", list(sip_inflows.columns))
print("\nMissing values per column:\n", sip_inflows.isnull().sum())
print("\nRows with any missing values:\n", sip_inflows[sip_inflows.isnull().any(axis=1)])

sip_clean = sip_inflows.copy()

print("\nExplanation: yoy_growth_pct is missing for Jan-Dec 2022 because")
print("year-over-year growth requires data from 12 months prior, which")
print("doesn't exist for the first year in the dataset. This is expected,")
print("not a data quality error, so these values are correctly left as null.")

sip_clean.to_csv("Data/Processed/monthly_sip_inflows_clean.csv", index=False)
print("\nSaved cleaned monthly_sip_inflows to Data/Processed/monthly_sip_inflows_clean.csv")

import shutil

clean_as_is = [
    "01_fund_master.csv",
    "03_aum_by_fund_house.csv",
    "05_category_inflows.csv",
    "06_industry_folio_count.csv",
    "09_portfolio_holdings.csv",
    "10_benchmark_indices.csv",
]

for filename in clean_as_is:
    src = "Data/Raw/" + filename
    dst = "Data/Processed/" + filename
    shutil.copy(src, dst)
    print("Copied:", filename)