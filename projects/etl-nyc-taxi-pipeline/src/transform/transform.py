import pandas as pd
import logging

def clean_column_names(df):
    """
    Clean and standardize column names by converting to lowercase, stripping whitespace, and replacing
    spaces with underscores. It should apply to all column names in the DataFrame to ensure consistency and avoid issues with case sensitivity or special characters.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame whose column names need to be cleaned.

    Returns
    -------
    pandas.DataFrame
        The DataFrame with cleaned column names.
    """
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    return df

def drop_unused_columns(df, columns_to_drop):
    """
    Drop specified columns from the DataFrame that are not needed for analysis.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame from which to drop columns.
    columns_to_drop : list of str
        A list of column names that should be dropped from the DataFrame.

    Returns
    -------
    pandas.DataFrame
        The DataFrame with the specified columns dropped.
    """
    existing_columns_to_drop = [col for col in columns_to_drop if col in df.columns]
    return df.drop(columns=existing_columns_to_drop)

def convert_datetime_columns(df, datetime_columns):
    """
    Convert specified columns in a DataFrame to datetime format.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the columns to be converted.
    datetime_columns : list of str
        A list of column names that should be converted to datetime format.

    Returns
    -------
    pandas.DataFrame
        The DataFrame with the specified columns converted to datetime format.
    """ 
    
    
    for col in datetime_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        else:
            missing_cols = [col for col in datetime_columns if col not in df.columns]
    logging.warning(f"The following columns were not found in the DataFrame and will be skipped: {missing_cols}")
    return df

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
    
    for col in numeric_columns:
        if col in df.columns:
            df[col] = df[col].round(decimals)
        else:
            missing_cols = [col for col in numeric_columns if col not in df.columns]
    logging.warning(f"The following columns were not found in the DataFrame and will be skipped: {missing_cols}")
    return df

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
    
    logging.info("finished transform stage")
    rows_after = len(df)
    logging.info(f"Number of rows after transformation: {rows_after}")
    
    rows_removed = rows_before - rows_after
    logging.info(f"Number of rows removed during transformation: {rows_removed}")
    
    return df