# CLAUDE.md — dbt-nyc-taxi

## Project Context

This is the transformation layer of a multi-stage data pipeline built on the NYC Taxi dataset.
It sits directly downstream of `etl-nyc-taxi-pipeline`, which handles ingestion from source
to BigQuery (Parquet via Python). This project takes that raw BigQuery data and applies
structured dbt transformations to produce analytics-ready models.

This project is part of a broader portfolio (`data-portfolio`) that demonstrates a full
modern data stack: ingestion → transformation → orchestration.

---

## Pipeline Evolution

| Layer         | Project                   | Status      |
|---------------|---------------------------|-------------|
| Ingestion/ETL | etl-nyc-taxi-pipeline     | Complete    |
| Transformation| dbt-nyc-taxi (this repo)  | In Progress |
| Orchestration | airflow-nyc-taxi (future) | Planned     |

---

## This Project's Goals

- Build a clean dbt transformation layer on top of existing BigQuery raw data
- Follow the staging → intermediate → mart model pattern
- Demonstrate analytics engineering best practices (modularity, testing, documentation)
- Serve as a portfolio artifact targeting Analytics Engineering roles

---

## Data Source

- Raw data lives in BigQuery, loaded by `etl-nyc-taxi-pipeline`
- Dataset: NYC Taxi Trip Records (public dataset)
- Target warehouse: BigQuery (Snowflake integration planned as a future extension)

---

## dbt Model Layer Conventions

Follow this pattern strictly:

```
models/
├── staging/        # 1:1 with source tables, light renaming and casting only
├── intermediate/   # Business logic, joins, and calculations
└── mart/           # Final analytics-ready tables for reporting
```

- Staging models: prefix with `stg_`
- Intermediate models: prefix with `int_`
- Mart models: no prefix, named for the business concept (e.g. `trips`, `revenue_by_zone`)

---

## Coding Conventions

- Python: modular, well-commented, with docstrings
- SQL: readable formatting, CTEs preferred over subqueries
- All models should have a corresponding `.yml` schema file with column descriptions and tests
- Use `not_null` and `unique` tests at minimum on primary keys
- Keep business logic out of staging models

---

## Career / Portfolio Notes

- This project targets Analytics Engineering roles (~65% of portfolio focus)
- Snowflake is a high-priority addition for future iterations (high AE job posting prevalence)
- Databricks, Kafka, and Spark are intentionally deprioritized for now
- Airflow orchestration is the planned next layer after this project is complete

---

## What Has Already Been Decided

- dbt project lives in its own folder (`dbt-nyc-taxi/`) within `data-portfolio/`
- Separation from the ETL project is intentional: each layer stands alone but references the others
- The repo-level README narrates the full pipeline story across all projects

---

## What To Avoid

- Do not modify anything in `etl-nyc-taxi-pipeline/` from this workspace
- Do not add orchestration logic here — that belongs in a future Airflow project
- Do not over-engineer staging models; keep them thin and focused
