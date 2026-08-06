import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///bluestock_mf.db")

def run_query(sql, description):
    print("\n" + "="*50)
    print(description)
    print("="*50)
    result = pd.read_sql(sql, engine)
    print(result)
    return result

q1 = """
SELECT dim_fund.scheme_name, dim_fund.fund_house, fact_performance.aum_crore
FROM fact_performance
JOIN dim_fund USING (amfi_code)
ORDER BY fact_performance.aum_crore DESC
LIMIT 5;
"""
run_query(q1, "Query 1: Top 5 Funds by AUM")

q2 = """
SELECT strftime('%Y-%m', date) AS year_month, AVG(nav_value) AS avg_nav
FROM fact_nav
WHERE amfi_code = 119551
GROUP BY year_month
ORDER BY year_month;
"""
run_query(q2, "Query 2: Average NAV per Month (SBI Bluechip)")

q3 = """
SELECT strftime('%Y', transaction_date) AS year, SUM(amount_inr) AS total_sip_amount
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY year
ORDER BY year;
"""
run_query(q3, "Query 3: SIP Year-over-Year Growth")

q4 = """
SELECT state, COUNT(*) AS num_transactions, SUM(amount_inr) AS total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_amount DESC;
"""
run_query(q4, "Query 4: Transactions by State")

q5 = """
SELECT dim_fund.scheme_name, dim_fund.fund_house, fact_performance.expense_ratio_pct
FROM fact_performance
JOIN dim_fund USING (amfi_code)
WHERE fact_performance.expense_ratio_pct < 1.0
ORDER BY fact_performance.expense_ratio_pct;
"""
run_query(q5, "Query 5: Funds with Expense Ratio Under 1%")

q3 = """
SELECT strftime('%Y', transaction_date) AS year, SUM(amount_inr) AS total_sip_amount
FROM fact_transactions
WHERE transaction_type = 'Sip'
GROUP BY year
ORDER BY year;
"""
run_query(q3, "Query 3: SIP Year-over-Year Growth")

q6 = """
SELECT dim_fund.scheme_name, fact_performance.return_3yr_pct, fact_performance.risk_grade
FROM fact_performance
JOIN dim_fund USING (amfi_code)
ORDER BY fact_performance.return_3yr_pct DESC
LIMIT 5;
"""
run_query(q6, "Query 6: Top 5 Funds by 3-Year Return")

q7 = """
SELECT payment_mode, COUNT(*) AS num_transactions, AVG(amount_inr) AS avg_amount
FROM fact_transactions
GROUP BY payment_mode
ORDER BY avg_amount DESC;
"""
run_query(q7, "Query 7: Average Transaction Amount by Payment Mode")

q8 = """
SELECT kyc_status, COUNT(*) AS num_investors
FROM fact_transactions
GROUP BY kyc_status;
"""
run_query(q8, "Query 8: KYC Status Breakdown")

q9 = """
SELECT fund_house, MAX(aum_crore) AS latest_aum_crore
FROM fact_aum
GROUP BY fund_house
ORDER BY latest_aum_crore DESC;
"""
run_query(q9, "Query 9: Fund Houses Ranked by AUM")

q10 = """
SELECT dim_fund.scheme_name, fact_performance.sharpe_ratio, fact_performance.category
FROM fact_performance
JOIN dim_fund USING (amfi_code)
ORDER BY fact_performance.sharpe_ratio DESC
LIMIT 5;
"""
run_query(q10, "Query 10: Top 5 Funds by Sharpe Ratio (Risk-Adjusted Return)")

