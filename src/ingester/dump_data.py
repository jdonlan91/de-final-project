import boto3


def generate_object_key(table_name, timestamp):
    return f"{table_name}-{timestamp}.csv"


def dump_data(table_name, timestamp, csv_data, bucket_name):
    """Dumps csv-formatted data into S3 bucket as .csv file

    File will be named '{table_name}-{timestamp}.csv'.
    Intended to be called by a parent AWS Lambda function.

    Args:
        table_name: name of table from which data was extracted.
        timestamp: timestamp when parent Lambda was called.
        csv_data: string of data in csv format.
        bucket_name: name of destination S3 bucket.

    Returns:
        The string "Data dumped successfully!"

    Raises:
        ClientError: an error occurred in accessing
        (or writing the file to) the named S3 bucket.

    """
    object_key = generate_object_key(table_name, timestamp)

    try:
        client = boto3.client("s3")

        response = client.put_object(
            Body=csv_data,
            Bucket=bucket_name,
            Key=object_key,
        )

        response_metadata = response["ResponseMetadata"]

        print(
            f"""
        HTTP status code: {response_metadata['HTTPStatusCode']}
        Timestamp: {response_metadata['HTTPHeaders']['last-modified']}
        """
        )

        return "Data dumped successfully!"

    except Exception as e:
        raise e
