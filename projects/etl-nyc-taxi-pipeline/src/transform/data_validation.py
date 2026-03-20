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
    
    #combine all below conditions into a single boolean to improve performance:
    mask = (
        df[required_columns].notnull().all(axis=1) &
        (df['passenger_count'] > 0) &
        (df['passenger_count'] <= 8) &
        (df['trip_distance'] > 0) &
        (df['fare_amount'] > 0)
    )
    df = df[mask]
        
    return df

def round_numeric_columns(df, numeric_columns, decimals=2):
    """
    Round specified numeric columns in a DataFrame to a given number of decimal places.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the numeric columns to be rounded.
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
                raise ValueError(f"{col} has {invalid_count} invalid values after conversion")

    return df