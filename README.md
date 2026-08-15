# Bluestock Mutual Fund Analytics Capstone

A 7-day end-to-end data analytics capstone project for Bluestock Fintech, covering data ingestion, cleaning, database design, exploratory data analysis, performance analytics, and an interactive Power BI dashboard for 40 AMFI-registered mutual fund schemes.

## Project Overview

This project analyzes ~87,000+ rows of mutual fund data (NAV history, investor transactions, scheme performance, AUM, SIP inflows) spanning 2022–2026, covering 40 schemes across 10 fund houses. It includes:

- A cleaned, validated dataset built from 10 raw AMFI CSV sources
- A SQLite star schema (2 dimension tables, 4 fact tables) for structured querying
- Exploratory data analysis (10+ charts) covering AUM trends, SIP growth, category inflows, and investor demographics
- Performance analytics: CAGR, Sharpe/Sortino ratios, Alpha/Beta (OLS regression vs. Nifty 100), Max Drawdown, and a composite Fund Scorecard
- A 4-page interactive Power BI dashboard with drill-through, slicers, and a custom date dimension

**Top-performing fund:** Mirae Asset Large Cap Fund (Fund Score: 86.25/100)

## Tech Stack

- **Python 3.14** — pandas, SQLAlchemy, statsmodels, matplotlib/plotly
- **SQLite** — star schema database (`bluestock_mf.db`)
- **Power BI Desktop** — dashboard and DAX measures
- **Jupyter Notebooks** — EDA and performance analytics

## Folder Structure

```
MutualFundAnalytics/
├── Data/
│   ├── Raw/              # Original AMFI CSVs (10 files)
│   └── Processed/        # Cleaned CSVs (_clean suffix)
├── Notebooks/
│   ├── EDA_Analysis.ipynb
│   └── performance_Analytics.ipynb
├── Scripts/
│   ├── data_ingestion.py
│   ├── data_cleaning.py
│   ├── database_setup.py
│   ├── run_queries.py
│   ├── live_nav_fetch.py
│   └── run_pipeline.py   # master script — runs the full ETL
├── SQL/
│   ├── schema.sql
│   ├── queries.sql
│   └── data_dictionary.md
├── Dashboard/
│   └── bluestock_mf_dashboard.pbix
├── reports/
│   ├── charts/            # EDA chart exports
│   ├── Final_Report.pdf
│   └── Bluestock_MF_Presentation.pptx
└── bluestock_mf.db        # SQLite database (generated)
```

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/haleemajanna/capstone-mutual-fund-analytics.git
   cd capstone-mutual-fund-analytics
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify folder structure** — ensure `Data/Raw/` contains the 10 source CSVs before running the pipeline.

## How to Run the ETL Pipeline

Run the full pipeline (ingestion → cleaning → database build → exploratory queries) from the **project root**:

```bash
python Scripts/run_pipeline.py
```

This will:
1. Load and validate the 10 raw CSVs
2. Clean and save processed datasets to `Data/Processed/`
3. Build the `bluestock_mf.db` SQLite star schema
4. Run 10 exploratory SQL queries against the database

**To run steps individually instead:**
```bash
python Scripts/data_ingestion.py
python Scripts/data_cleaning.py
python Scripts/database_setup.py
python Scripts/run_queries.py
```

**Optional — refresh live NAV data** (calls the mfapi.in public API; overwrites existing raw NAV files, so run separately and deliberately):
```bash
python Scripts/live_nav_fetch.py
```

**Notebooks** (run after the pipeline, using Jupyter or VS Code):
- `Notebooks/EDA_Analysis.ipynb` — exploratory analysis and chart generation
- `Notebooks/performance_Analytics.ipynb` — CAGR, Sharpe/Sortino, Alpha/Beta, Fund Scorecard

## How to Open the Dashboard

1. Install [Power BI Desktop](https://powerbi.microsoft.com/desktop/) (free, Windows only)
2. Open `Dashboard/bluestock_mf_dashboard.pbix`
3. If prompted to refresh data, click **Refresh** — the dashboard reads directly from the CSVs in `Data/Processed/` and `Data/Raw/`
4. Navigate using the page tabs at the bottom:
   - **Industry Overview** — AUM, SIP inflows, folios, scheme count
   - **Fund Performance** — return vs. risk scatter, fund scorecard, NAV growth
   - **Investor Analytics** — transactions by state, SIP/Lumpsum/Redemption split, demographics
   - **SIP & Market Trends** — SIP inflow vs. Nifty50, category heatmap, top categories by inflow
5. Right-click any fund in the scorecard table (Page 2) and select **Drill through → Fund NAV Detail** for a per-fund deep dive

## Dataset Descriptions

| Dataset | Description | Rows |
|---|---|---|
| `01_fund_master.csv` | Fund metadata — house, category, plan, expense ratio, manager | 40 |
| `02_nav_history.csv` | Daily NAV per scheme | ~46,000 |
| `03_aum_by_fund_house.csv` | Quarterly AUM by fund house | 90 |
| `04_monthly_sip_inflows.csv` | Industry-wide monthly SIP inflow trends | 48 |
| `05_category_inflows.csv` | Net inflows by fund category | 144 |
| `06_industry_folio_count.csv` | Quarterly investor folio counts | 21 |
| `07_scheme_performance.csv` | Returns, risk ratios, expense ratio per scheme | 40 |
| `08_investor_transactions.csv` | Individual investor transaction records | ~32,800 |
| `09_portfolio_holdings.csv` | Underlying stock holdings per scheme | 322 |
| `10_benchmark_indices.csv` | Daily Nifty50/Nifty100 index values | 8,050 |

Cleaned versions of the above (where applicable) are suffixed `_clean` and saved to `Data/Processed/`.

## Author

Haleema Janna— Data Analyst (Fresher) | [GitHub](https://github.com/haleemajanna)

---
*Capstone project completed as part of the Bluestock Fintech remote internship program.*
