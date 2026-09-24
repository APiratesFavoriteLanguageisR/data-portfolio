# Project Overview

This project is the transformation layer of a multi-stage data pipeline built on the NYC Taxi public dataset. Sitting directly downstream of etl-nyc-taxi-pipeline, it uses dbt to apply structured SQL transformations across three model layers: staging, intermediate, and mart. The result is a clean, analytics-ready dataset that serves as the foundation for exploratory analysis of taxi fare patterns, trip characteristics, and tipping behavior.

# Tech Stack

- dbt 2.0 (Fusion engine) — transformation framework used to transition a cleaned dataset into an analytics-ready dataset.
- BigQuery — cloud data warehouse target where models are materialized (production path).
- DuckDB — local, in-process database target for running the project without cloud setup (dev path). Adapter is in beta for dbt v2.
- dbt-utils — dbt package used for surrogate key generation (`generate_surrogate_key`). A surrogate key was needed due to the absence of a usable primary key.
- Python / pip — for managing the dbt environment and installing dependencies.
- Git / GitHub — version control

# Model Architecture

This project features a three layer pattern: staging, intermediate, and mart layers.

## Staging Layer

The staging layer mirrors the raw source table (from BigQuery or the local DuckDB file, depending on the target), applying light transformations including column selection, data type standardization, and surrogate key generation via `dbt_utils.generate_surrogate_key`.

**Models:**
- `stg_yellow_trips.sql`

## Intermediate Layer

The intermediate layer enriches each trip record with three purpose-built models: payment type labeling, time of day bucketing, and trip distance categorization.

**Models:**
- `int_payment_type.sql`
- `int_time_buckets.sql`
- `int_trip_categorization.sql`

## Mart Layer

The mart layer model joins all upstream models into a final table that can be used for analysis.

**Models:**
- `mart_trips.sql`

A lineage graph screenshot can be seen below:

![Lineage graph](images/lineage_graph.png)

# How to Run

## Prerequisites (all paths)

- Clone the repo
- Create and activate a virtual environment (recommended, keeps dependencies isolated):
  - `python -m venv .venv`
  - `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Mac/Linux)
- Python 3.9+
- Install dbt v2 via `pip install dbt` (installation docs: https://docs.getdbt.com/)
- Install project dependencies with `pip install -r requirements.txt`
- Configure your dbt profile: copy `profiles.example.yml` to `~/.dbt/profiles.yml` and fill in your values

There are two ways to run this project. **The DuckDB path requires no cloud account and is the fastest way to get running.** The BigQuery path is optional and only needed to run against the cloud warehouse.

## Option A: Local run with DuckDB (no cloud required)

Runs the entire project locally against a DuckDB file, no Google Cloud account, credentials, or warehouse setup needed.

1. Obtain the raw data as a Parquet file (produced by the upstream `etl-nyc-taxi-pipeline` project).
2. Load the Parquet into a local DuckDB file:
   - `python scripts/load_parquet_to_duckdb.py --parquet path/to/yellow_trips.parquet`
   - This creates `dev.duckdb` in the project root.
3. In `~/.dbt/profiles.yml`, set the `dev` target's `path` to your `dev.duckdb` location.
4. Build the project: `dbt build --target dev`

> Note: the DuckDB adapter for dbt v2 is currently in beta.

## Option B: BigQuery (optional, cloud)

Runs against BigQuery instead of DuckDB. Requires your own Google Cloud setup.

- A Google Cloud project with the BigQuery API enabled
- A service account key with BigQuery permissions
- `GOOGLE_APPLICATION_CREDENTIALS` set to your key file path
- The raw `yellow_trips` table must exist in your BigQuery `portfolio_nyc_taxi` dataset (run the `etl-nyc-taxi-pipeline` project first)
- Configure the `prod` target in `~/.dbt/profiles.yml` with your project and keyfile
- Build the project: `dbt build --target prod`

## Running models, tests, and docs

The commands below work for either path. Add `--target dev` for DuckDB or `--target prod` for BigQuery (if omitted, dbt uses the default target set in your `profiles.yml`).

**Models**
- Run all models: `dbt run --target dev`
- Run a specific model: `dbt run -s mart_trips --target dev`

**Tests**
- Run all tests: `dbt test --target dev`
- Run a specific model's tests: `dbt test -s mart_trips --target dev`

**Docs**
- Generate and serve: `dbt docs generate --target dev` then `dbt docs serve`

> `dbt build` runs models and tests together. `dbt run` and `dbt test` are for running them separately.

# Key Findings

The main focus of the analyses conducted was regarding January 2022 taxi fares and if they differed by time or day. The overall finding was that there was not much variance, however there were still some interesting findings.

- When comparing fares by days of the week, interestingly there was not a significant difference [range: $12.15 - $13.72]. That being said, Friday and Sunday tended to trend on the higher side, while Saturday tended to trend lower, showing the disparity between seemingly similar days.
- There also was not a significant difference when comparing taxi fares by weekends vs weekdays.
- The pattern changes, however, when comparing taxi fares by time of day. Some interesting findings show that early mornings (5am - 8am) have the highest fare [$14.03], while trips during the morning rush (8 am - 11am) showed the lowest fare as well as tips. The highest average tips are found in taxi trips that are performed overnight (10 pm - 5 am).
- One last analysis, this time comparing tips by days of the week, show that Sunday is the day that sees the highest average tips [$2.55], while Wednesday sees the lowest average.

# What is Next

- Now that the pipeline is complete, the next step is to schedule and monitor it using Apache Airflow.
- Once Airflow is added, the full process from extraction to final analysis will be fully fleshed out.
- One note on further analyses: this project currently only focuses on a small subset of data for convenience. A more complete analysis would include a much bigger sample, including more months and years. Perhaps the findings would change and produce even more interesting insights.
