"""
Simple Fund Recommender

Takes a risk appetite (Low / Moderate / High) and prints the top 3 funds
by Sharpe ratio within that matching risk_grade.
"""

import pandas as pd
from sqlalchemy import create_engine

DB_PATH = "sqlite:///bluestock_mf.db"


def recommend(risk_appetite):
    engine = create_engine(DB_PATH)
    query = """
    SELECT dim_fund.scheme_name, dim_fund.fund_house, fact_performance.sharpe_ratio,
           fact_performance.risk_grade, fact_performance.return_3yr_pct
    FROM fact_performance
    JOIN dim_fund USING (amfi_code)
    WHERE fact_performance.risk_grade = ?
    ORDER BY fact_performance.sharpe_ratio DESC
    LIMIT 3;
    """
    result = pd.read_sql(query, engine, params=(risk_appetite,))
    return result


def main():
    print("Fund Recommender")
    print("Risk appetite options: Low, Moderate, High, Very High")
    risk_appetite = input("Enter risk appetite: ").strip()

    result = recommend(risk_appetite)
    if result.empty:
        print(f"No funds found for risk_grade = '{risk_appetite}'.")
    else:
        print(f"\nTop 3 funds for '{risk_appetite}' risk appetite:\n")
        print(result.to_string(index=False))


if __name__ == "__main__":
    main()