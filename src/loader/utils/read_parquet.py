import pyarrow.parquet as pq


def read_parquet(file_name, bucket_name):
    """Reads the contents of a parquet file in an AWS S3 bucket.

    Args:
        file_name <string> the name of the parquet file.
        bucket_name <string> the name of the S3 bucket containing the file.

    Returns:
        <str> the contents of the parquet file in csv format.
    """
    pass
