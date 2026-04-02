import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

def remove_invalid_rows(df, required_columns):
    """
    Remove rows from the DataFrame that contain null values in specified required columns, a passenger_count outside of a reasonable range, 
    contain a fare amount <= 0, or contain a trip distance <= 0.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame from which to remove invalid rows.
    required_columns : list of str
        A list of column names that must not contain null values for a row to be considered valid.

    Returns
    -------
    pandas.DataFrame
        The DataFrame with invalid rows removed.
    """
    
    invalid_nulls = (~df[required_columns].notnull().all(axis=1)).sum()
    invalid_passenger_low = (df['passenger_count'] <= 0).sum()
    invalid_passenger_high = (df['passenger_count'] > 8).sum()
    invalid_distance = (df['trip_distance'] <= 0).sum()
    invalid_fare = (df['fare_amount'] <= 0).sum()
    invalid_datetime = (df['pickup_datetime'] >= df['dropoff_datetime']).sum()
    
    logging.info(f"Rows removed due to nulls: {invalid_nulls}")
    logging.info(f"Rows removed due to passenger_count <= 0: {invalid_passenger_low}")
    logging.info(f"Rows removed due to passenger_count > 8: {invalid_passenger_high}")
    logging.info(f"Rows removed due to trip_distance <= 0: {invalid_distance}")
    logging.info(f"Rows removed due to fare_amount <= 0: {invalid_fare}")
    logging.info(f"Rows removed due to pickup_datetime >= dropoff_datetime: {invalid_datetime}")
    logging.info(f"Total rows removed: {invalid_nulls + invalid_passenger_low + invalid_passenger_high + invalid_distance + invalid_fare + invalid_datetime}")
    
    #combine all below conditions into a single boolean to improve performance:
    mask = (
        df[required_columns].notnull().all(axis=1) &
        (df['passenger_count'] > 0) &
        (df['passenger_count'] <= 8) &
        (df['trip_distance'] > 0) &
        (df['fare_amount'] > 0) &
        (df['pickup_datetime'] < df['dropoff_datetime'])
    )
    df = df[mask]
        
    return df

def enforce_numeric_types(df, numeric_columns):
    """
    Convert specified columns in a DataFrame to numeric types and coerce invalid values to NaN.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the numeric columns to be converted.
    numeric_columns : list of str
        A list of column names that should be rounded.
    decimals : int, optional
        The number of decimal places to round to (default is 2).

    Returns
    -------
    pandas.DataFrame
        The DataFrame with the specified numeric columns rounded.
    """
    
    missing_cols = [col for col in numeric_columns if col not in df.columns]
    
    if missing_cols:
        logging.warning(
            f"The following columns were not found in the DataFrame and will be skipped: {missing_cols}"
        )

    # Convert only columns that exist
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            
    for col in numeric_columns:
        if col in df.columns:
            invalid_count = df[col].isna().sum()
            if invalid_count > 0:
                logging.warning(f"{col} has {invalid_count} invalid values after conversion")

    return df