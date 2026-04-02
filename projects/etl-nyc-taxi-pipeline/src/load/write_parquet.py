import logging
import os
import pyarrow as pa
import pyarrow.parquet as pq


def write_parquet(df, output_path):
    """
    Write a DataFrame to a Parquet file using PyArrow.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to write.
    output_path : str
        The file path where the Parquet file will be saved.
    """

    logging.info(f"Writing DataFrame to Parquet file at {output_path}")

    # Ensure correct file extension
    if not output_path.endswith(".parquet"):
        logging.warning(f"Output path {output_path} does not end with .parquet. Adding extension.")
        output_path += ".parquet"

    # Ensure directory exists (if a directory is specified)
    dir_path = os.path.dirname(output_path)
    if dir_path and not os.path.exists(dir_path):
        logging.info(f"Directory {dir_path} does not exist. Creating directory.")
        os.makedirs(dir_path)

    try:
        # Convert DataFrame to PyArrow Table and write to Parquet
        table = pa.Table.from_pandas(df, preserve_index=False)
        pq.write_table(table, output_path, compression="snappy")

        logging.info(f"Parquet file successfully written to {output_path}")
        logging.info(f"Rows written: {len(df)}")

    except (OSError, pa.ArrowInvalid) as e:
        logging.error(f"Error writing Parquet file: {e}")
        raise