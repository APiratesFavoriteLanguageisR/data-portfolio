import argparse
import yaml
import logging
import os
from typing import Any, Dict, List
import copy

def parse_args():
    argparser = argparse.ArgumentParser(description="ETL Pipeline for NYC Taxi Data")
    argparser.add_argument("--project_id", type=str, help="Google Cloud project ID")
    argparser.add_argument("--dataset_id", type=str, help="BigQuery dataset ID")
    argparser.add_argument("--bq_public_table", type=str, help="BigQuery public table name")
    argparser.add_argument("--start_date", type=str, help="Start date for data extraction (YYYY-MM-DD)")
    argparser.add_argument("--end_date", type=str, help="End date for data extraction (YYYY-MM-DD)")
    argparser.add_argument("--write_disposition", type=str, help="Write disposition for BigQuery table")
    return argparser.parse_args()


def load_config():
        
        project_root = os.path.dirname(os.path.dirname(__file__))
        yaml_path = os.path.join(project_root, "config", "config.yaml")

        if not os.path.exists(yaml_path):
            print(f"Warning: config.yaml not found at {yaml_path}. Using config.example.yaml instead.")
            yaml_path = os.path.join(project_root, "config", "config.example.yaml")

        try:
            with open(yaml_path, "r", encoding="utf-8") as file:
                configs = yaml.safe_load(file)
                return configs
        except FileNotFoundError:
            raise RuntimeError(f"Configuration file not found at {yaml_path}. Please ensure it exists.")
        except yaml.YAMLError as e:
            raise RuntimeError(f"Error parsing YAML configuration: {e}")


def merge_config(configs: dict, args: argparse.Namespace):
    merged = copy.deepcopy(configs)
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
    args = parse_args()
    configs = load_config()
    if configs is None:
        raise RuntimeError("Configuration could not be loaded.")
    resolved_configs = merge_config(configs, args)
    logging.basicConfig(format='{asctime} - {levelname} - {message}', style='{', level=logging.INFO)
    logging.info(f"Resolved Configurations: {resolved_configs}")



if __name__ == "__main__":
    main()