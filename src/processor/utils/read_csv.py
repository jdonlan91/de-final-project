import boto3


def read_csv(file_name, bucket_name):
    s3 = boto3.client("s3")
    response = s3.get_object(
        Bucket=bucket_name,
        Key=file_name
    )
    file_data = response['Body'].read().decode('utf-8').split('\n')
    keys = file_data[0].split(',')
    rows = [row.strip().split(',') for row in file_data[1:]]

    return [dict(zip(keys, row)) for row in rows]
