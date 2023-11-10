import boto3


def fetch_new_files(bucket_name, timestamp):
    """
    retrieves files that have not been loaded into the database,

    Args:
        bucket_name <str> the name of the bucket.
        timestamp <str> the timestamp when the loader lambda was invoked

    Returns:
        <list> a list of all files that have not been loaded.
    """

    s3 = boto3.client("s3")
    response = s3.list_objects_v2(Bucket=bucket_name)
    print(response['Content'])

    
