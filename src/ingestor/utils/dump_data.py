import boto3


def generate_object_key(table_name, timestamp):
    timestamp_string = timestamp.strftime("%d-%m-%Y-%H%M%S")
    date = timestamp_string[:10]
    return f"{table_name}/{date}/{timestamp_string}.csv"


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

    try:

        filename = generate_object_key(table_name, timestamp)
        client = boto3.client("s3")

        client.put_object(
            Body=csv_data,
            Bucket=bucket_name,
            Key=filename,
        )

        return filename

    except Exception as e:
        raise e
