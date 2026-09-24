"""
load_parquet_to_duckdb.py

Loads the ETL's Parquet output into a local DuckDB file so the dbt
DuckDB (dev) target can read it as an ordinary table. This sidesteps the
Fusion bundled driver's lack of parquet-extension support: Fusion reads a
native DuckDB table, not the Parquet directly.

Revisit at DuckDB-adapter GA — the bundled driver may then read Parquet
directly, letting this pre-step be removed.

Usage:
    # from the dbt project root
    python scripts/load_parquet_to_duckdb.py --parquet path/to/yellow_trips.parquet

    # optional: override the DuckDB output path
    python scripts/load_parquet_to_duckdb.py --parquet path/to/file.parquet --duckdb custom.duckdb
"""

import argparse
import os
from pathlib import Path

import duckdb

# --- Fixed targets: must match the dbt source definition ---
TARGET_SCHEMA = "portfolio_nyc_taxi"   # matches the dbt source's `schema`
TARGET_TABLE = "yellow_trips"          # matches the dbt source's table name

# Anchor the default DuckDB path to the PROJECT ROOT (parent of scripts/),
# so the file lands in the same place no matter where the script is invoked from.
# __file__ -> scripts/ -> project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DUCKDB = PROJECT_ROOT / "dev.duckdb"


def load_parquet_to_duckdb(parquet_path: str, duckdb_path: str) -> None:
    """Create schema.table in a DuckDB file from a Parquet file, replacing if present.

    The load is idempotent: re-running rebuilds the table cleanly rather than
    appending or erroring.

    Args:
        parquet_path: Path to the source Parquet file (the ETL's output).
        duckdb_path: Path to the DuckDB file to create or overwrite.

    Raises:
        FileNotFoundError: If the Parquet file does not exist.
    """
    # Fail early with a clear message instead of a cryptic DuckDB error
    if not os.path.isfile(parquet_path):
        raise FileNotFoundError(f"Parquet file not found: {parquet_path}")

    con = duckdb.connect(duckdb_path)
    try:
        # DuckDB reads Parquet natively via read_parquet(); no extension load needed.
        # Parameterized (?) to avoid path-quoting issues, especially on Windows.
        con.execute(f"CREATE SCHEMA IF NOT EXISTS {TARGET_SCHEMA};")
        con.execute(
            f"""
            CREATE OR REPLACE TABLE {TARGET_SCHEMA}.{TARGET_TABLE} AS
            SELECT * FROM read_parquet(?);
            """,
            [parquet_path],
        )
        row_count = con.execute(
            f"SELECT COUNT(*) FROM {TARGET_SCHEMA}.{TARGET_TABLE};"
        ).fetchone()[0]
        print(f"Loaded {row_count:,} rows into {TARGET_SCHEMA}.{TARGET_TABLE} in {duckdb_path}")
    finally:
        con.close()


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Load the ETL's Parquet output into a local DuckDB file for the dbt dev target."
    )
    parser.add_argument(
        "--parquet",
        required=True,
        help="Path to the source Parquet file (the ETL's output).",
    )
    parser.add_argument(
        "--duckdb",
        default=str(DEFAULT_DUCKDB),
        help="Path to the DuckDB file to write (default: dev.duckdb in the dbt project root).",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    load_parquet_to_duckdb(args.parquet, args.duckdb)