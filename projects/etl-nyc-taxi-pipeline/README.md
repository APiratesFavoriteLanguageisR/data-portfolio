# NYC Taxi ETL Pipeline

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

## Key Challenges



## Technologies
Python
Pandas
BigQuery
YAML configuration

## Setup

1. Clone the repository
2. Copy the example configuration

    cp config/config.example.yaml config/config.yaml

3. Update the configuration with your environment settings

## Future Improvements
Feature engineering
Load stage
Pipeline orchestration improvements
