import pandas as pd
import pyarrow as pa


def convert_to_parquet(list_of_dictionaries):
    """Converts list of dictionaries to parquet table.

    Takes a list of dictionaries from transform_data
    and converts it to a parquet format table.

    Args:
        list_of_dictionaries

    Returns:
        parquet table

    Raises:
        Exception.
    """
    df = pd.DataFrame(list_of_dictionaries)
    parquet_table = pa.Table.from_pandas(df)
    return parquet_table
