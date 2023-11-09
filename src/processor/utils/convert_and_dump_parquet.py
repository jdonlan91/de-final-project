import boto3
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from io import BytesIO


def generate_object_key(table_name, timestamp):
    timestamp_string = timestamp.strftime("%d-%m-%Y-%H%M%S")
    date = timestamp_string[:10]
    return f"{table_name}/{date}/{timestamp_string}.parquet"


def convert_and_dump_parquet(table_name, timestamp,
                             transformed_data, bucket_name):
    """Converts list of dictionaries to pyarrow table
    and dump the parquet file into the processed bucket.

    Takes a list of dictionaries from transform_data
    and converts it to a pyarrow table.

    Args:

        table_name: name of table from which data was extracted.
        timestamp: timestamp when parent Lambda was called.
        transformed_data: list of dictionaries from transform_data
        bucket_name: name of destination S3 bucket.

    Returns:
        parquet file name

    Raises:
        Exception.
    """
    try:
        file_name = generate_object_key(table_name, timestamp)
        client = boto3.client("s3")

        df = pd.DataFrame(transformed_data)
        parquet_table = pa.Table.from_pandas(df)

        stream = BytesIO()
        pq.write_table(parquet_table, stream)

        client.put_object(
            Body=stream.getvalue(),
            Bucket=bucket_name,
            Key=file_name)

        return file_name

    except Exception as e:
        raise e