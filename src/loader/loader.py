from datetime import datetime
import json
import logging

import boto3

from src.loader.utils.seed_dim_date import seed_dim_date
from src.loader.utils.fetch_new_files import fetch_new_files
from src.loader.utils.read_parquet import read_parquet
from src.loader.utils.populate_schema import populate_schema


logger = logging.getLogger("Loader logger")
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """
    Loads data from processed bucket into prepared warehouse.
    Triggered by eventbridge every (5) minutes.

    Calls get_previous_invocation to check if lambda has been
    previously invoked:
    - if first invocation then call fetch_new_files
        with a very old timestamp
    - if previously invoked then call fetch_new_files
        with the timestamp of the previous invocation.

    for each new file:

    call read_parquet on the file
    load the data into the appropriate table (populate_schema)
    in the destination warehouse
"""
    db_credentials = get_db_credentials()

    prev_invocation = get_previous_invocation(
        '/aws/lambda/loader', 'loader_history')
    this_invocation = datetime.fromisoformat(
        event["timestamp"])
    bucket_name = event["bucket_name"]
    long_time_ago = datetime.strptime(
        "01-01-2001-000000", "%d-%m-%Y-%H%M%S")
    cutoff = long_time_ago if prev_invocation is None else prev_invocation

    if cutoff == long_time_ago:
        seed_dim_date(db_credentials)

    new_file_names = fetch_new_files(bucket_name, cutoff)
    if new_file_names == []:
        logger.info("No new files.")
    else:
        for file_name in new_file_names:
            csv_string = read_parquet(file_name, bucket_name)
            result = populate_schema(db_credentials, file_name, csv_string)
            logger.info(result)

    log_invocation_time(
            this_invocation, '/aws/lambda/loader', 'loader_history')


def get_db_credentials():
    secret_name = "postgres_db_credentials"
    region_name = "eu-west-2"

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager",
                            region_name=region_name)

    get_secret_value_response = client.get_secret_value(SecretId=secret_name)

    secret = json.loads(get_secret_value_response["SecretString"])
    db_credentials = {}
    db_credentials["DB_HOST"] = secret["host"]
    db_credentials["DB_USERNAME"] = secret["username"]
    db_credentials["DB_PASSWORD"] = secret["password"]
    db_credentials["DB_NAME"] = secret["dbname"]

    return db_credentials


def log_invocation_time(timestamp, log_group, log_stream):
    conn = boto3.client("logs", region_name="eu-west-2")
    event = [
        {
            'timestamp': int(datetime.now().timestamp() * 1000),
            'message': timestamp.strftime("%d-%m-%Y-%H%M%S")
        }
    ]
    conn.put_log_events(
        logGroupName=log_group, logStreamName=log_stream, logEvents=event)


def get_previous_invocation(log_group, log_stream):
    conn = boto3.client("logs", region_name="eu-west-2")
    log_events = conn.get_log_events(
        logGroupName=log_group, logStreamName=log_stream)['events']

    if len(log_events) == 0:
        return None
    else:
        return datetime.strptime(log_events[-1]['message'], "%d-%m-%Y-%H%M%S")
