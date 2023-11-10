import io

import boto3
import pandas
import pyarrow.parquet as pq


def read_parquet(file_name, bucket_name):
    """Reads the contents of a parquet file in an AWS S3 bucket.

    Args:
        file_name <string> the name of the parquet file.
        bucket_name <string> the name of the S3 bucket containing the file.

    Returns:
        <str> the contents of the parquet file in csv format.
    """
    buffer = io.BytesIO()
    s3 = boto3.resource('s3')

    object = s3.Object(bucket_name, file_name)
    object.download_fileobj(buffer)

    dataframe = pandas.read_parquet(buffer)
    csv_data = dataframe.to_csv(index=False)

    if csv_data == '\n':
        return ''
    else:
        return csv_data
