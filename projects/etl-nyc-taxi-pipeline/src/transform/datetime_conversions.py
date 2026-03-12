import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

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
    
    
    missing_cols = [col for col in datetime_columns if col not in df.columns]

    if missing_cols:
        logging.warning(
            f"The following columns were not found in the DataFrame and will be skipped: {missing_cols}"
        )

    # Convert only columns that exist
    for col in datetime_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df

