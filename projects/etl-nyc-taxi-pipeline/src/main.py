"""
main.py

This module serves as the entry point for the NYC Taxi ETL pipeline.

Responsibilities
----------------
1. Parse optional command line arguments.
2. Load the base configuration from a YAML file.
3. Merge command line overrides with the configuration file.
4. Initialize logging for the pipeline.
5. Execute the extraction stage of the pipeline.

Design Philosophy
-----------------
Configuration is driven primarily by YAML files to ensure reproducibility.
Command line arguments are optional overrides that allow flexible execution
without modifying configuration files.

Example execution:

python main.py --start_date 2022-01-01 --end_date 2022-01-31
"""

import argparse
import yaml
import logging
import os
from typing import Any, Dict, List
import copy
from extract import extract_data
from transform import transform_data
import time
from utils.pipeline_utils import run_stage

# Initialize logging for the pipeline
logging.basicConfig(
    format='{asctime} - {levelname} - {message}',
    style='{',
    level=logging.INFO
)

def parse_args():
    
    """
    Parse command line arguments that may override configuration settings.

    These parameters allow the pipeline to be executed with different inputs
    without modifying the configuration YAML file.

    Returns
    -------
    argparse.Namespace
        Object containing parsed command line arguments.
    """
    
    argparser = argparse.ArgumentParser(
        description="ETL Pipeline for NYC Taxi Data"
    )
    
    argparser.add_argument(
        "--project_id",
        type=str,
        help="Google Cloud project ID"
    )
    
    argparser.add_argument(
        "--dataset_id",
        type=str,
        help="BigQuery dataset ID"
    )
    
    argparser.add_argument(
        "--bq_public_table",
        type=str, help="BigQuery public table name"
    )
    
    argparser.add_argument(
        "--start_date",
        type=str,
        help="Start date for data extraction (YYYY-MM-DD)"
    )
    
    argparser.add_argument(
        "--end_date", 
        type=str, 
        help="End date for data extraction (YYYY-MM-DD)"
    )
    
    argparser.add_argument(
        "--write_disposition",
        type=str, 
        help="Write disposition for BigQuery table"
    )
    
    return argparser.parse_args()


def load_config():
        
    """
    Load the pipeline configuration from YAML.

    The function attempts to load `config.yaml`. If that file is not present,
    it falls back to `config.example.yaml`. This allows the repository to
    include a template configuration without exposing environment-specific
    settings.

    Returns
    -------
    dict
        Dictionary containing configuration values used by the pipeline.
    """
    # Determine project root directory dynamically
    # This allows the script to run regardless of current working directory
    project_root = os.path.dirname(os.path.dirname(__file__))
    
    yaml_path = os.path.join(project_root, "config", "config.yaml")

    # If the real configuration file is missing, fall back to the example config
    if not os.path.exists(yaml_path):
        logging.warning(
            f"Warning: config.yaml not found at {yaml_path}. "
            "Using config.example.yaml instead."
        )
        yaml_path = os.path.join(project_root, "config", "config.example.yaml")

    try:
        with open(yaml_path, "r", encoding="utf-8") as file:
            configs = yaml.safe_load(file)
            return configs
        
    except FileNotFoundError:
        raise RuntimeError(
            f"Configuration file not found at {yaml_path}. "
            "Please ensure it exists."
        )
        
    except yaml.YAMLError as e:
        raise RuntimeError(
            f"Error parsing YAML configuration: {e}"
        )


def merge_config(configs: dict, args: argparse.Namespace):
    
    """
    Merge configuration file values with command line overrides.

    Command line arguments take precedence over YAML configuration values.
    This allows the same pipeline configuration to be reused across
    different executions.

    Parameters
    ----------
    configs : dict
        Base configuration loaded from YAML.

    args : argparse.Namespace
        Command line arguments that may override configuration values.

    Returns
    -------
    dict
        Final resolved configuration dictionary used by the pipeline.
    """
    
    # Create a deep copy to avoid mutating the original configuration
    merged = copy.deepcopy(configs)
    
    # Override configuration values if CLI arguments were provided
    if args.project_id is not None:
        merged["gcp"]["project_id"] = args.project_id
        
    if args.dataset_id is not None:
        merged["gcp"]["dataset_id"] = args.dataset_id
        
    if args.bq_public_table is not None:
        merged["source"]["bq_public_table"] = args.bq_public_table
        
    if args.start_date is not None:
        merged["source"]["start_date"] = args.start_date
        
    if args.end_date is not None:
        merged["source"]["end_date"] = args.end_date
        
    if args.write_disposition is not None:
        merged["runtime"]["write_disposition"] = args.write_disposition
        
    return merged


def main():
    
    """
    Main execution function for the ETL pipeline.

    Workflow
    --------
    1. Parse command line arguments
    2. Load YAML configuration
    3. Merge CLI overrides
    4. Initialize logging
    5. Execute extraction stage
    """
    
    pipeline_start = time.time()
    
    # Parse optional command line arguments
    args = parse_args()
    
    # Load configuration from YAML
    configs = load_config()
    logging.debug(f"Configuration loaded: {configs}")
    
    if configs is None:
        raise RuntimeError("Configuration could not be loaded.")
    
    # Merge CLI overrides into configuration
    resolved_configs = merge_config(configs, args)
    
    logging.info("Pipeline initialization complete.")
    
    logging.info(
        f"Pipeline started | source_table={resolved_configs['source']['bq_public_table']} "
        f"| start_date={resolved_configs['source']['start_date']} "
        f"| end_date={resolved_configs['source']['end_date']}"
    )

    raw_data = run_stage("Extract", extract_data, resolved_configs)
    
    logging.info("Data extraction completed.")
    
    clean_data = run_stage("Transform", transform_data, raw_data, resolved_configs)
    
    logging.info("Data transformation completed.")
    
    pipeline_end = time.time()
    
    logging.info(
        f"Pipeline completed successfully | Total runtime: {pipeline_end - pipeline_start:.2f} seconds"
    )

if __name__ == "__main__":
    main()