"""
load_to_bigquery.py

This script is responsible for loading the transformed DataFrame into a BigQuery table. 
It uses the Google Cloud BigQuery client library to perform the load operation. 
The function `load_to_bigquery` takes in the cleaned DataFrame and the pipeline configuration,
and writes the data to the specified BigQuery table. This modular design allows for easy
maintenance and scalability of the loading logic, and can be reused across different pipelines or datasets in the future.

Note: Ensure that the Google Cloud credentials are properly set up in the environment where this script is executed, 
and that the BigQuery API is enabled for the project.
"""

from google.cloud import bigquery
import logging

def load_to_bigquery(df, config):
    
    """
    Load data into a BigQuery table.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing the data to be loaded.
    config : dict
        Dictionary containing resolved pipeline configuration including:
            project ID - config['gcp']['project_id'],
            dataset ID - config['gcp']['dataset_id'],
            table ID - config['gcp']['table_id']
            write_disposition - config['runtime']['write_disposition']

    Raises
    ------
    Exception
        If there is an error during the loading process, an exception will be raised with the error details.
        
    Notes
    -----
    Config must contain gcp and runtime keys.
    Google credentials are expected via GOOGLE_APPLICATION_CREDENTIALS or default ADC.

    Returns
    -------
    None
    """
    try:
        logging.info(f"Loading data into {config['gcp']['project_id']}.{config['gcp']['dataset_id']}.{config['gcp']['table_id']}")
        logging.info(f"Project ID from config: {config['gcp']['project_id']}")
        logging.info(f"Initializing BigQuery client for project: {config['gcp']['project_id']}")

        client = bigquery.Client(project=config["gcp"]["project_id"])

        # Configure the load job to automatically detect the schema and specify the write disposition based on the configuration.
        job_config = bigquery.LoadJobConfig(
            autodetect=True,
            write_disposition=config['runtime']['write_disposition']     
        )


        ### Make a BigQuery API request to load the data from the DataFrame into the specified BigQuery table.
        destination = f"{config['gcp']['project_id']}.{config['gcp']['dataset_id']}.{config['gcp']['table_id']}"
        job = client.load_table_from_dataframe(
            df, destination, num_retries=5, job_config=job_config
            )

        job.result()
        ### Fetch loaded table metadata.
        table = client.get_table(destination)  

        logging.info(f"Loaded {table.num_rows} rows into {config['gcp']['dataset_id']}.{config['gcp']['table_id']}.")
        
    except Exception as e:
        logging.error(f"Error loading data into BigQuery: {e}")
        raise