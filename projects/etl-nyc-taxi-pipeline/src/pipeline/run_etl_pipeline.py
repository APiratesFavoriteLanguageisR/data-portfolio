import logging
import time
import os

from src.extract.extract_bq import extract_data
from src.transform.transform_pipeline import transform_data 
from src.utils.pipeline_utils import run_stage
from src.load.write_parquet import write_parquet

def run_pipeline(resolved_configs):
    
    pipeline_start = time.time()
    
    logging.info(
        f"Pipeline started | source_table={resolved_configs['source']['bq_public_table']} "
        f"| start_date={resolved_configs['source']['start_date']} "
        f"| end_date={resolved_configs['source']['end_date']}"
    )

    raw_data = run_stage(
        "Extract",
        extract_data,
        resolved_configs
    )
    
    logging.info("Data extraction completed.")
    
    clean_data = run_stage(
        "Transform",
        transform_data,
        raw_data,
        resolved_configs
    )
    
    logging.info("Data transformation completed.")
    
    file_name = resolved_configs["filename"]["mart"].format(
        start_date=resolved_configs["source"]["start_date"],
        end_date=resolved_configs["source"]["end_date"]
    )
    output_path = os.path.join(resolved_configs["output"]["output_path"], file_name)
    
    run_stage(
        "Load",
        write_parquet,
        clean_data,
        output_path
    )
    
    logging.info(f"Data loading completed. Parquet file written to {output_path}")
    
    pipeline_end = time.time()
    
    logging.info(
        f"Pipeline completed successfully | Total runtime: {pipeline_end - pipeline_start:.2f} seconds"
    )
    
    return clean_data