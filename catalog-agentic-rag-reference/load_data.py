"""Load both Excel catalogs into one SQLite file (catalog.db). Run once."""
import sqlite3
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent.parent / "catalog-agentic-rag" / "data"
DB_PATH = Path(__file__).parent / "catalog.db"
COMPANY_FILES = {
    "circuitnova": "electronics_catalog.xlsx",
    "hearthwell": "home_appliances_catalog.xlsx",
}

DB_PATH.unlink(missing_ok=True)
with sqlite3.connect(DB_PATH) as connection:
    for company_prefix, file_name in COMPANY_FILES.items():
        sheets = pd.read_excel(DATA_DIR / file_name, sheet_name=None)
        for sheet_name, frame in sheets.items():
            # Store dates as plain YYYY-MM-DD text so SQL comparisons are simple.
            for column_name in frame.columns:
                if pd.api.types.is_datetime64_any_dtype(frame[column_name]):
                    frame[column_name] = frame[column_name].dt.strftime("%Y-%m-%d")
            table_name = f"{company_prefix}_{sheet_name}"
            frame.to_sql(table_name, connection, index=False)
            print(f"{table_name}: {len(frame)} rows")
