CREATE TABLE dim_fund (
	amfi_code BIGINT, 
	fund_house TEXT, 
	scheme_name TEXT, 
	category TEXT, 
	sub_category TEXT, 
	"plan" TEXT, 
	launch_date TEXT, 
	expense_ratio_pct FLOAT, 
	fund_manager TEXT, 
	risk_category TEXT, 
	sebi_category_code TEXT
);

CREATE TABLE dim_date (
	date DATETIME, 
	year INTEGER, 
	month INTEGER, 
	quarter INTEGER, 
	day_of_week TEXT, 
	is_weekend BOOLEAN
);

CREATE TABLE fact_nav (
	date DATETIME, 
	amfi_code BIGINT, 
	nav_value FLOAT
);

CREATE TABLE fact_transactions (
	investor_id TEXT, 
	transaction_date TEXT, 
	amfi_code BIGINT, 
	transaction_type TEXT, 
	amount_inr BIGINT, 
	state TEXT, 
	city TEXT, 
	city_tier TEXT, 
	age_group TEXT, 
	gender TEXT, 
	annual_income_lakh FLOAT, 
	payment_mode TEXT, 
	kyc_status TEXT
);

CREATE TABLE fact_performance (
	amfi_code BIGINT, 
	scheme_name TEXT, 
	fund_house TEXT, 
	category TEXT, 
	"plan" TEXT, 
	return_1yr_pct FLOAT, 
	return_3yr_pct FLOAT, 
	return_5yr_pct FLOAT, 
	benchmark_3yr_pct FLOAT, 
	alpha FLOAT, 
	beta FLOAT, 
	sharpe_ratio FLOAT, 
	sortino_ratio FLOAT, 
	std_dev_ann_pct FLOAT, 
	max_drawdown_pct FLOAT, 
	aum_crore BIGINT, 
	expense_ratio_pct FLOAT, 
	morningstar_rating BIGINT, 
	risk_grade TEXT
);

CREATE TABLE fact_aum (
	date TEXT, 
	fund_house TEXT, 
	aum_lakh_crore FLOAT, 
	aum_crore BIGINT, 
	num_schemes BIGINT
);
