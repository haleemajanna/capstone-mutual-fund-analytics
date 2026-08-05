# Data Dictionary — Bluestock Mutual Fund Analytics

## dim_fund
One row per mutual fund scheme (40 total).

| Column | Type | Description |
|---|---|---|
| amfi_code | INTEGER | Unique AMFI scheme code (Primary Key) |
| fund_house | TEXT | Asset management company running the fund |
| scheme_name | TEXT | Full name of the scheme |
| category | TEXT | Equity or Debt |
| sub_category | TEXT | e.g. Large Cap, Small Cap, Gilt, Liquid |
| plan | TEXT | Regular or Direct plan |
| launch_date | TEXT | Date the scheme was launched |
| expense_ratio_pct | REAL | Annual fee charged by the fund, as % of assets |
| fund_manager | TEXT | Name of the fund manager |
| risk_category | TEXT | Risk level (Low, Moderate, High, Very High) |
| sebi_category_code | TEXT | SEBI's official classification code |

## dim_date
One row per calendar date, covering the full NAV history range.

| Column | Type | Description |
|---|---|---|
| date | TEXT | Calendar date (Primary Key) |
| year | INTEGER | Year extracted from date |
| month | INTEGER | Month number (1-12) |
| quarter | INTEGER | Quarter number (1-4) |
| day_of_week | TEXT | Name of the weekday |
| is_weekend | INTEGER | 1 if Saturday/Sunday, else 0 |

## fact_nav
Daily NAV per fund, including forward-filled weekends/holidays. Source: mfapi.in + provided nav_history.csv.

| Column | Type | Description |
|---|---|---|
| amfi_code | INTEGER | Links to dim_fund |
| date | TEXT | Links to dim_date |
| nav_value | REAL | Net Asset Value (price per unit) on that date |

## fact_transactions
Individual investor transaction records.

| Column | Type | Description |
|---|---|---|
| investor_id | TEXT | Unique investor identifier |
| transaction_date | TEXT | Date of transaction |
| amfi_code | INTEGER | Links to dim_fund |
| transaction_type | TEXT | Sip, Lumpsum, or Redemption |
| amount_inr | INTEGER | Transaction amount in Indian Rupees |
| state | TEXT | Investor's state |
| city | TEXT | Investor's city |
| city_tier | TEXT | City classification (Tier 1/2/3) |
| age_group | TEXT | Investor's age bracket |
| gender | TEXT | Investor's gender |
| annual_income_lakh | REAL | Investor's annual income, in lakhs INR |
| payment_mode | TEXT | UPI, Cheque, Mandate, or Net Banking |
| kyc_status | TEXT | Verified or Pending |

## fact_performance
Performance and risk metrics per fund, as of latest available data.

| Column | Type | Description |
|---|---|---|
| amfi_code | INTEGER | Links to dim_fund (Primary Key) |
| return_1yr_pct / return_3yr_pct / return_5yr_pct | REAL | Historical returns over each period |
| benchmark_3yr_pct | REAL | Benchmark index's 3-year return for comparison |
| alpha | REAL | Excess return vs benchmark, risk-adjusted |
| beta | REAL | Fund's volatility relative to the market |
| sharpe_ratio | REAL | Return earned per unit of risk taken |
| sortino_ratio | REAL | Like Sharpe, but only penalizes downside volatility |
| std_dev_ann_pct | REAL | Annualized standard deviation (volatility) |
| max_drawdown_pct | REAL | Largest peak-to-trough decline observed |
| aum_crore | INTEGER | Assets Under Management, in crore INR |
| expense_ratio_pct | REAL | Annual fee as % of assets |
| morningstar_rating | INTEGER | Star rating (1-5) |
| risk_grade | TEXT | Risk classification |

## fact_aum
AUM by fund house over time.

| Column | Type | Description |
|---|---|---|
| date | TEXT | Reporting date |
| fund_house | TEXT | Asset management company |
| aum_lakh_crore | REAL | AUM in lakh crore INR |
| aum_crore | INTEGER | AUM in crore INR |
| num_schemes | INTEGER | Number of schemes offered by this fund house |

## Data Sources
- AMFI India (public scheme data)
- mfapi.in (live NAV API)
- Provided datasets: Bluestock Fintech capstone project files