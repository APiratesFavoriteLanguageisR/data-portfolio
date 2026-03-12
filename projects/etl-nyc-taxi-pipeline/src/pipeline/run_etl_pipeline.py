import logging
import time

from src.extract.extract_bq import extract_data
from src.transform.transform_pipeline import transform_data 
from src.utils.pipeline_utils import run_stage

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
    
    pipeline_end = time.time()
    
    logging.info(
        f"Pipeline completed successfully | Total runtime: {pipeline_end - pipeline_start:.2f} seconds"
    )
    
    return clean_data