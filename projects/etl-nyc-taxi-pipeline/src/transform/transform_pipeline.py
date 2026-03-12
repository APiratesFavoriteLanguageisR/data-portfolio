import pandas as pd
import logging
from .clean_columns import clean_column_names, drop_unused_columns
from .datetime_conversions import convert_datetime_columns
from .data_validation import remove_invalid_rows, round_numeric_columns
from .feature_engineering import apply_feature_engineering

def transform_data(df, configs):
    """
    Apply transformations to the DataFrame.

    This function can be expanded to include specific transformations related to date handling,
    such as extracting year, month, day, or creating new features based on date columns.
    """
    
    logging.info("starting transform stage")
    rows_before = len(df)
    logging.info(f"Number of rows before transformation: {rows_before}")
    
    df = clean_column_names(df)
    df = drop_unused_columns(df, configs["transform"]["drop_columns"])
    df = convert_datetime_columns(df, configs["transform"]["datetime_columns"])
    df = remove_invalid_rows(df, configs["transform"]["required_columns"])
    df = round_numeric_columns(df, configs["transform"]["numeric_columns"])
    df = apply_feature_engineering(df)
    
    logging.info("finished transform stage")
    rows_after = len(df)
    logging.info(f"Number of rows after transformation: {rows_after}")
    
    rows_removed = rows_before - rows_after
    logging.info(f"Number of rows removed during transformation: {rows_removed}")
    
    return df