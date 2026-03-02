# NYC Taxi ETL Pipeline (BigQuery → Python → BigQuery)

## Overview
This project implements a parameterized ETL pipeline that extracts NYC Taxi trip data from a public BigQuery dataset for a configurable date range, performs data quality validation and transformation in Python, and loads the results into a layered BigQuery design (raw, staging, mart).

## Key Features
- Extract from public BigQuery source table using SQL and a date range parameter
- Config-driven pipeline with optional CLI overrides
- Layered warehouse outputs: raw → staging → mart
- Data quality checks and row count auditing
- Logging for reproducibility and traceability

## Reproducibility and Credentials
This repository does not include credentials. To run the pipeline, create a GCP project, enable the BigQuery API, and authenticate using `GOOGLE_APPLICATION_CREDENTIALS` (service account key stored locally and excluded from git).

## Configuration
Copy `config.example.yaml` to `config.yaml` and fill in your GCP project details. You can override config values via CLI arguments once the pipeline scripts are added.

## Outputs
The pipeline writes three tables to your BigQuery dataset:
- raw_yellow_trips
- stg_yellow_trips
- mart_yellow_trips
