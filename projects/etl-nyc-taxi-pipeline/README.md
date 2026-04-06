# NYC Taxi ETL Pipeline

## Why This Project

This project demonstrates the design and implementation of a modular, production-style ETL pipeline, with a focus on data quality, configurability, and scalability.

## Overview
This project implements a modular, config-driven ETL pipeline using NYC taxi trip data.

The pipeline extracts data from the BigQuery public dataset, applies data cleaning and validation transformations, and produces an analytics-ready dataset. The final output is stored in Parquet format for efficient downstream analysis.

The pipeline is designed with clear separation of concerns across extraction, transformation, validation, and load stages.

## Architecture

The pipeline follows a modular Extract → Transform → Load (ETL) architecture designed to convert raw data into analytics-ready datasets.

### Extract Stage
- NYC Taxi trip data is extracted from a BigQuery public dataset using parameters defined in a configuration file.
- The extraction process includes logging of row counts and sample data for validation and debugging.

### Transform Stage
- A modular transformation pipeline is applied to clean, validate, and enrich the dataset. This stage is composed of the following components:

  - **clean_columns**
    - Standardizes column names and removes unnecessary fields.

  - **data_validation**
    - Applies data quality rules to remove invalid records.
    - Enforces numeric type consistency for specified columns.

  - **datetime_conversions**
    - Converts designated columns into proper datetime formats for time-based analysis.

  - **feature_engineering**
    - Creates derived features including:
      - Trip duration (in minutes)
      - Time-based attributes from pickup datetime
      - Fare-per-mile metric

### Load Stage
- The final transformed dataset is written to a Parquet file using PyArrow.
- Parquet is used to preserve schema and enable efficient, columnar storage for downstream analytics.

## Key Features

- **Modular Pipeline Design**
  - Clear separation of extract, transform, and load stages for maintainability and scalability.

- **Config-Driven Execution**
  - Pipeline behavior (data source, date ranges, output paths, file naming) is controlled via YAML configuration, with support for runtime overrides.

- **Robust Logging and Stage Tracking**
  - Each pipeline stage is wrapped with timing and logging utilities to provide visibility into execution and performance.

- **Data Validation Layer**
  - Enforces data quality rules, including null handling, range checks, and logical constraints (e.g., pickup time before dropoff time).

- **Type Enforcement and Error Handling**
  - Ensures correct data types using controlled coercion and validation checks, with warnings for data inconsistencies.

- **Feature Engineering**
  - Generates derived metrics such as trip duration, time-based features, and fare-per-mile for downstream analysis.

- **Parquet Output with PyArrow**
  - Writes columnar, compressed Parquet files optimized for analytics workloads.

- **Separation of Concerns**
  - Distinct modules for extraction, transformation, validation, and loading improve readability and extensibility.

- **Reusable Utility Functions**
  - Common functionality (e.g., stage execution, logging) is abstracted into reusable components.

- **Integration with BigQuery Public Dataset**
  - Demonstrates ability to extract and process data from cloud-based data sources using the BigQuery API.

## Data Validation Rules

The following data quality rules are applied during the transformation stage to ensure the dataset is suitable for analysis:

- **trip_distance > 0**  
  Removes records with non-positive trip distances.

- **fare_amount > 0**  
  Filters out trips with zero or negative fares.

- **1 ≤ passenger_count ≤ 8**  
  Ensures passenger counts fall within a realistic range.

- **pickup_datetime < dropoff_datetime**  
  Enforces logical trip sequencing.

- **Required columns must not be null**  
  Rows with missing values in critical fields are removed.

## Key Challenge: Debugging Data Type Issues in Feature Engineering

One of the primary challenges encountered during this project stemmed from a subtle but impactful data type issue within the transformation stage.

During feature engineering, the calculation of a fare-per-mile metric repeatedly failed. Initial inspection did not immediately reveal the cause, so additional logging was introduced to trace the issue. This revealed that the relevant columns had incorrect data types: `fare_amount` was stored as an object, while `trip_distance` had been incorrectly converted to a datetime.

Using the debugger to step through the transformation pipeline, the root cause was identified. In the `datetime_conversions` module, `trip_distance` had been mistakenly included in the list of columns to convert, resulting in an invalid type transformation.

After correcting this, attention turned to `fare_amount`, which required explicit type enforcement. This was resolved by incorporating the column into a custom `enforce_numeric_types` function, ensuring consistent numeric conversion with validation checks.

Once both columns were correctly typed, the fare-per-mile calculation executed successfully.

This issue highlighted the importance of:
- careful data type management in ETL pipelines  
- validating transformation steps incrementally  
- using logging and debugging tools to isolate root causes  

## Tech Stack

- Python  
- Pandas  
- PyArrow  
- Google BigQuery  
- YAML (configuration management)  
- Logging (Python standard library)

## Setup

1. Clone the repository:
   1. git clone https://github.com/APiratesFavoriteLanguageisR/data-portfolio.git
2. Copy the example configuration file:
   1. cp config/config.example.yaml config/config.yaml
3. Update `config.yaml` with your environment settings:
- BigQuery project ID  
- Date range parameters  
- Output path  

4. Create and activate a virtual environment:
   1. python -m venv .venv
5. Install required dependencies:
   1. pip install -r requirements.txt
6. Run the pipeline from the project root directory:
   1. python -m src.main
7. Run the test suite:
   python -m pytest tests/ -v


## Output

The pipeline generates a Parquet file containing an analytics-ready dataset.

- File name is dynamically generated based on the selected date range  
(e.g., `mart_yellow_trips_2022-01-01_to_2022-01-31.parquet`)
- Output is stored in the configured output directory  
- Data is written using PyArrow with columnar compression for efficient storage and analysis  


## Tests

The pipeline includes a unit test suite covering the core transformation logic.

- **`tests/test_data_validation.py`** — Validates every filter rule in `remove_invalid_rows` and type coercion behavior in `enforce_numeric_types`
- **`tests/test_feature_engineering.py`** — Verifies correctness of derived features: trip duration, time attributes, and fare-per-mile
- **`tests/test_clean_columns.py`** — Confirms column name standardization and safe column dropping
- **`tests/test_datetime_conversions.py`** — Checks datetime conversion, invalid coercion to NaT, and graceful handling of missing columns

Run all tests from the project root:
  python -m pytest tests/ -v