import logging

def extract_data(config: dict):
    """
    Extract data from the source specified in the config.

    Args:
        config (dict): Configuration dictionary containing source information.

    Returns:
        data: Extracted data.
    """
    # log public table and date range for extraction
    #import logging and use logging.info to log the message instead of print
    logging.info(f"Extracting data from {config['source']['bq_public_table']}"
                 f" for date range {config['source']['start_date']} to {config['source']['end_date']}")
    
    data = None  # Replace with actual extraction code
    return data
