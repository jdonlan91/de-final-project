import logging
import json
from datetime import datetime

import boto3
from botocore.exceptions import ClientError
from pg8000.exceptions import InterfaceError

from utils.convert_to_csv import convert_to_csv
from utils.dump_data import dump_data
from utils.fetch_new_data import fetch_new_data
from utils.fetch_table_names import fetch_table_names

logger = logging.getLogger("Ingestor logger")
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """Fetches new data from all tables in source database,
    formats them in CSV files and dumps those files
      into an Ingested S3 bucket

    Triggered by Eventbridge (scheduled once every 5 mins)

    Calls fetch_new_data on every table
    If no new data fetched then this lambda stops execution
    If new data, calls convert_to_csv to get CSV-formatted string
    Then passes this string to dump_data to put .csv file in S3 bucket
    Logs metadata about files added to the bucket
    Logs any errors that occur
    """

    try:
        db_credentials = get_db_credentials()
        table_names = fetch_table_names(db_credentials)

        prev_invocation = get_previous_invocation(
            '/aws/lambda/ingestor', 'ingestor_history')
        this_invocation = datetime.fromisoformat(
            event["timestamp"])
        bucket_name = event["bucket_name"]
        long_time_ago = datetime.strptime(
            "01-01-2001-000000", "%d-%m-%Y-%H%M%S")
        cutoff = long_time_ago if prev_invocation is None else prev_invocation

        for table_name in table_names:
            new_table_data = fetch_new_data(table_name,
                                            cutoff, db_credentials)
            logger.info(f"Table name: {table_name}.")
            if len(new_table_data) == 0:
                logger.info("No new data found.")
                continue
            else:
                csv_string = convert_to_csv(new_table_data)
                filename = dump_data(table_name,
                                     this_invocation, csv_string, bucket_name)
                logger.info(f"Fetched {len(new_table_data)} rows of new data.")
                logger.info(f"File {filename} added to bucket {bucket_name}")

        log_invocation_time(
            this_invocation, '/aws/lambda/ingestor', 'ingestor_history')

    except InterfaceError:
        logger.error("Error interacting with source database")
    except ClientError as c:
        if c.response["Error"]["Code"] == "ResourceNotFoundException":
            logger.error(
                "Error getting database credentials from Secrets Manager.")
        elif c.response["Error"]["Code"] == "NoSuchBucket":
            logger.error("Error writing file to ingested bucket.")
        else:
            logger.error(
                f"""AWS client error {c.response['Error']['Code']}.
{c.response['Error']['Message']}."""
            )
    except Exception as e:
        logger.error("Unexpected error occurred.")
        logger.error(e)


def get_db_credentials():
    secret_name = "totesys_db_credentials"
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
