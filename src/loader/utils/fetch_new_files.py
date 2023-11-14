import boto3
from datetime import datetime


def fetch_new_files(bucket_name, timestamp):
    """
    retrieves files that have not been loaded into the database,

    Args:
        bucket_name <str> the name of the bucket.
        timestamp <str> the timestamp when the loader lambda was invoked

    Returns:
        <list> a list of all files that have not been loaded.
    """

    response = get_all_file_names(bucket_name)
    list_of_parquet_files = []
    for contents in response["Contents"]:
        last_modified_time = contents["LastModified"].replace(tzinfo=None)
        if last_modified_time > timestamp:
            list_of_parquet_files.append(contents["Key"])
    sorted_files = sort_new_files(list_of_parquet_files)
    return sorted_files


def get_all_file_names(bucket_name):
    s3 = boto3.client("s3")
    response = s3.list_objects_v2(Bucket=bucket_name)
    return response


def sort_new_files(file_names):
    def sort_by_timestamp_then_table_name(file_name):
        timestamp = file_name[-25:-8]
        table_name = file_name.split("/")[0]
        return (datetime.strptime(timestamp, "%d-%m-%Y-%H%M%S"), table_name)
    sorted_files = sorted(file_names, key=sort_by_timestamp_then_table_name)
    return sorted_files
