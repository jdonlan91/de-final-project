import boto3
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from io import BytesIO


def generate_object_key(filename):
    table_name_converter = {
        'design': 'dim_design',
        'staff': 'dim_staff',
        'counterparty': 'dim_counterparty',
        'currency': 'dim_currency',
        'sales_order': 'fact_sales_order',
        'address': 'dim_location'
    }
    old_table_name = filename.split('/')[0]
    new_table_name = table_name_converter[old_table_name]
    date = filename.split('/')[1]
    timestamp = filename.split('/')[2][:-4]
    return f"{new_table_name}/{date}/{timestamp}.parquet"


def convert_and_dump_parquet(filename,
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
        new_file_name = generate_object_key(filename)
        client = boto3.client("s3")

        df = pd.DataFrame(transformed_data)
        parquet_table = pa.Table.from_pandas(df)

        stream = BytesIO()
        pq.write_table(parquet_table, stream)

        client.put_object(
            Body=stream.getvalue(),
            Bucket=bucket_name,
            Key=new_file_name)

        return new_file_name

    except Exception as e:
        raise e
