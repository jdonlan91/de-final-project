from datetime import datetime
import json

import boto3


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

    fetch_new_files gets the names of the files that have been newly
    added to the processed bucket: needs to return
    a list of filenames sorted by loading order.

    for each new file:

    call read_parquet on the file
    load the data into the appropriate table (populate_schema) in the destination warehouse
"""

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
