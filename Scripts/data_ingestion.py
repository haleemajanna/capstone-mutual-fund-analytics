"""
Day 1 - Data Ingestion & Quality Check

Loads all raw AMFI mutual fund CSVs from Data/Raw/, validates that every
fund in the fund master has matching NAV history, and writes a summary
report to reports/day1_data_quality_summary.txt.
"""

import pandas as pd
import os
import glob

RAW_DIR = "Data/Raw"


def load_datasets():
    """Load every CSV in RAW_DIR into a dict keyed by filename (no extension)."""
    csv_files = glob.glob(os.path.join(RAW_DIR, "*.csv"))
    datasets = {}
    for filepath in csv_files:
        name = os.path.basename(filepath).replace(".csv", "")
        datasets[name] = pd.read_csv(filepath)
    print(f"Loaded {len(datasets)} datasets from {RAW_DIR}")
    return datasets


def validate_amfi_codes(datasets):
    """Check that every fund in fund_master has matching NAV history records."""
    fund_master = datasets["01_fund_master"]
    nav_history = datasets["02_nav_history"]

    fund_master_codes = set(fund_master["amfi_code"].unique())
    nav_history_codes = set(nav_history["amfi_code"].unique())
    missing_nav = fund_master_codes - nav_history_codes

    print(f"Total funds in fund_master: {len(fund_master_codes)}")
    print(f"Total funds with NAV history: {len(nav_history_codes)}")
    print(f"Funds missing NAV history: {len(missing_nav)}")

    return fund_master, fund_master_codes, nav_history_codes, missing_nav


def write_summary(datasets, fund_master, fund_master_codes, nav_history_codes, missing_nav):
    """Write the Day 1 data quality summary to reports/day1_data_quality_summary.txt."""
    conclusion = (
        "All 40 schemes in fund_master have matching NAV history records. "
        "No missing-code issues found."
        if not missing_nav
        else f"{len(missing_nav)} scheme(s) in fund_master are missing NAV history."
    )

    summary_lines = [
        "DAY 1 - DATA QUALITY SUMMARY",
        "=" * 40,
        "",
        f"Total datasets loaded: {len(datasets)}",
        f"Total funds in fund_master: {len(fund_master_codes)}",
        f"Total funds with NAV history: {len(nav_history_codes)}",
        f"Funds missing NAV history: {len(missing_nav)}",
        "",
        "Fund houses covered: " + ", ".join(fund_master['fund_house'].unique()),
        "Categories covered: " + ", ".join(fund_master['category'].unique()),
        "",
        f"Conclusion: {conclusion}",
    ]

    with open("reports/day1_data_quality_summary.txt", "w") as f:
        f.write("\n".join(summary_lines))

    print("Summary saved to reports/day1_data_quality_summary.txt")


def main():
    datasets = load_datasets()
    fund_master, fund_master_codes, nav_history_codes, missing_nav = validate_amfi_codes(datasets)
    write_summary(datasets, fund_master, fund_master_codes, nav_history_codes, missing_nav)


if __name__ == "__main__":
    main()