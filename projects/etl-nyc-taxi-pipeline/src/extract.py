"""
extract.py

This module implements the extraction stage of the NYC Taxi ETL pipeline.

Purpose
-------
The extraction layer is responsible for retrieving raw data from the
configured source system. In this project, the source system is the
public NYC Taxi dataset hosted in Google BigQuery.

Responsibilities
----------------
- Connect to the data source
- Execute a query against the configured dataset
- Filter records based on the configured date range
- Return the raw query results for downstream processing

Design Notes
------------
The extraction logic is intentionally isolated from the rest of the
pipeline. This separation allows new data sources (APIs, SFTP, or other
databases) to be added in the future without modifying the orchestration
logic in `main.py`.
"""

from google.cloud import bigquery
import logging

def extract_data(config: dict):
    
    """
    Extract data from the configured BigQuery source.

    Parameters
    ----------
    config : dict
        Dictionary containing resolved pipeline configuration including
        project ID, source table, and extraction date range.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing extracted dataset.
    """
    
    logging.info(f"Extracting data from {config['source']['bq_public_table']}"
        f" for date range {config['source']['start_date']} "
        f"to {config['source']['end_date']}"
    )
    
    
    logging.info(f"Project ID from config: {config['gcp']['project_id']}")
    # Initialize BigQuery client using the configured project ID.
    # The project acts as the execution context for queries.
    logging.info(f"Initializing BigQuery client for project: {config['gcp']['project_id']}")
    project_id = config["gcp"]["project_id"]
    client = bigquery.Client(project=project_id)
        
    # Construct SQL query to extract filtered taxi records.
    query = f"""
        SELECT *
        FROM `{config['source']['bq_public_table']}`
        WHERE pickup_datetime BETWEEN TIMESTAMP('{config['source']['start_date']}') AND TIMESTAMP('{config['source']['end_date']}')
        LIMIT 1000
    """
    logging.info("Executing BigQuery extraction query.")
    
    # Execute the query and fetch results
    query_job = client.query(query)
    data = query_job.to_dataframe()
    
    logging.info(
        f"Query executed successfully. Rows extracted: {len(data)}"
    )
    
    logging.info("Sample of extracted data:")
    logging.info(f"\n{data.head(5)}")   
    
    return data

    
