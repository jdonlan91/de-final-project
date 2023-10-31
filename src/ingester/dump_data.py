# Arguments: table_name, string of data in CSV format

# Returns: a string indicating success, possibly containing metadata about the file that has been dumped ad the bucket it has been dumped to.

# Dumps CSV data into ingestion bucket.

# s3://ingestion/table-name-timestamp.csv

import boto3

client = boto3.client("s3")


def genereate_object_key(table_name, timestamp):
    return f"{table_name}-{timestamp}.csv"


def dump_data(table_name, timestamp, csv_data, bucket_name):
    """
    DOCSTRING GOES HERE
    """
    object_key = genereate_object_key(table_name, timestamp)

    try:
        response = client.put_object(
            Body=csv_data,
            Bucket=bucket_name,
            Key=object_key,
        )

        response_metadata = response["ResponseMetadata"]

        response_string = f"""
        HTTP status code: {response_metadata['HTTPStatusCode']}
        Timestamp: {response_metadata['HTTPHeaders']['last-modified']}
        """

        if response_metadata["HTTPStatusCode"] == 200:
            print(response_string)
            return "Data dumped successfully!"

        return response
    except Exception as e:
        print(e)
