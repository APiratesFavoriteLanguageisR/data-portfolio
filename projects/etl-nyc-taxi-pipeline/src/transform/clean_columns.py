import logging

logging.basicConfig(level=logging.INFO)

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