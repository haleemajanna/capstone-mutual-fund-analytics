"""
Master Pipeline Script

Runs the full Bluestock Mutual Fund Analytics ETL pipeline end-to-end:
  1. data_ingestion   - load raw CSVs and validate AMFI codes
  2. data_cleaning    - clean and save processed CSVs
  3. database_setup   - build the bluestock_mf.db SQLite star schema
  4. run_queries      - run the 10 exploratory SQL queries

Usage (run from the PROJECT ROOT, e.g. C:\MutualFundAnalytics):
    python Scripts/run_pipeline.py

Note: live_nav_fetch.py is intentionally NOT included here, since it calls
a live external API and would overwrite the existing raw NAV CSVs on every
run. Run it manually and separately if a fresh NAV pull is needed:
    python Scripts/live_nav_fetch.py
"""

import os
import sys
import time

# Allow "import data_ingestion" etc. to work even though this script is
# run from the project root, not from inside Scripts/.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import data_ingestion
import data_cleaning
import database_setup
import run_queries


def main():
    start = time.time()

    print("\n" + "#" * 60)
    print("# STEP 1/4: DATA INGESTION")
    print("#" * 60)
    data_ingestion.main()

    print("\n" + "#" * 60)
    print("# STEP 2/4: DATA CLEANING")
    print("#" * 60)
    data_cleaning.main()

    print("\n" + "#" * 60)
    print("# STEP 3/4: DATABASE SETUP")
    print("#" * 60)
    database_setup.main()

    print("\n" + "#" * 60)
    print("# STEP 4/4: EXPLORATORY QUERIES")
    print("#" * 60)
    run_queries.main()

    elapsed = time.time() - start
    print("\n" + "#" * 60)
    print(f"# PIPELINE COMPLETE in {elapsed:.1f} seconds")
    print("#" * 60)


if __name__ == "__main__":
    main()