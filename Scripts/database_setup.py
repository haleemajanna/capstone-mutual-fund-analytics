"""
Day 2 - SQLite Star Schema Setup

Builds the bluestock_mf.db SQLite database from the cleaned/processed CSVs.
Creates 2 dimension tables (dim_fund, dim_date) and 4 fact tables
(fact_nav, fact_transactions, fact_performance, fact_aum).
"""

import pandas as pd
from sqlalchemy import create_engine

DB_PATH = "sqlite:///bluestock_mf.db"


def build_dim_fund(engine):
    """Build dim_fund from the raw fund master CSV."""
    fund_master = pd.read_csv("Data/Raw/01_fund_master.csv")
    dim_fund = fund_master[[
        "amfi_code", "fund_house", "scheme_name", "category",
        "sub_category", "plan", "launch_date", "expense_ratio_pct",
        "fund_manager", "risk_category", "sebi_category_code"
    ]].copy()
    dim_fund.to_sql("dim_fund", engine, if_exists="replace", index=False)
    print("dim_fund loaded:", len(dim_fund), "rows")
    return dim_fund


def build_dim_date(engine):
    """Build dim_date spanning the full NAV history date range, with calendar attributes."""
    nav_clean = pd.read_csv("Data/Processed/nav_history_clean.csv")
    nav_clean["date"] = pd.to_datetime(nav_clean["date"])

    all_dates = pd.date_range(nav_clean["date"].min(), nav_clean["date"].max(), freq="D")
    dim_date = pd.DataFrame({"date": all_dates})
    dim_date["year"] = dim_date["date"].dt.year
    dim_date["month"] = dim_date["date"].dt.month
    dim_date["quarter"] = dim_date["date"].dt.quarter
    dim_date["day_of_week"] = dim_date["date"].dt.day_name()
    dim_date["is_weekend"] = dim_date["date"].dt.dayofweek >= 5

    dim_date.to_sql("dim_date", engine, if_exists="replace", index=False)
    print("dim_date loaded:", len(dim_date), "rows")
    return nav_clean, dim_date


def build_fact_nav(engine, nav_clean):
    """Build fact_nav from cleaned NAV history."""
    fact_nav = nav_clean.rename(columns={"nav": "nav_value"})
    fact_nav.to_sql("fact_nav", engine, if_exists="replace", index=False)
    print("fact_nav loaded:", len(fact_nav), "rows")


def build_fact_transactions(engine):
    """Build fact_transactions from cleaned investor transactions."""
    txn_clean = pd.read_csv("Data/Processed/investor_transactions_clean.csv")
    txn_clean.to_sql("fact_transactions", engine, if_exists="replace", index=False)
    print("fact_transactions loaded:", len(txn_clean), "rows")


def build_fact_performance(engine):
    """Build fact_performance from cleaned scheme performance data."""
    perf_clean = pd.read_csv("Data/Processed/scheme_performance_clean.csv")
    perf_clean.to_sql("fact_performance", engine, if_exists="replace", index=False)
    print("fact_performance loaded:", len(perf_clean), "rows")


def build_fact_aum(engine):
    """Build fact_aum from raw AUM-by-fund-house data."""
    aum = pd.read_csv("Data/Raw/03_aum_by_fund_house.csv")
    aum.to_sql("fact_aum", engine, if_exists="replace", index=False)
    print("fact_aum loaded:", len(aum), "rows")


def main():
    engine = create_engine(DB_PATH)
    print("Database engine created: bluestock_mf.db")

    build_dim_fund(engine)
    nav_clean, _ = build_dim_date(engine)
    build_fact_nav(engine, nav_clean)
    build_fact_transactions(engine)
    build_fact_performance(engine)
    build_fact_aum(engine)


if __name__ == "__main__":
    main()