from datetime import datetime, timedelta
from src.ingestor.utils.convert_to_csv import convert_to_csv
from src.ingestor.utils.dump_data import dump_data
from src.ingestor.utils.fetch_new_data import fetch_new_data
import logging
import boto3
from botocore.exceptions import ClientError
import json
from pg8000.exceptions import InterfaceError

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
        table_names = [
            "sales_order",
            "design",
            "currency",
            "staff",
            "counterparty",
            "address",
            "department",
            "purchase_order",
            "payment_type",
            "payment",
            "transaction",
        ]

        timestamp = datetime.fromisoformat(
            event["timestamp"]) - timedelta(minutes=5)
        bucket_name = event["bucket_name"]
        db_credentials = get_db_credentials()

        for table_name in table_names:
            new_table_data = fetch_new_data(table_name,
                                            timestamp, db_credentials)
            logger.info(f"Table name: {table_name}.")
            if len(new_table_data) == 0:
                logger.info("No new data found.")
                continue
            else:
                csv_string = convert_to_csv(new_table_data)
                filename = dump_data(table_name, timestamp,
                                     csv_string, bucket_name)
                logger.info(f"Fetched {len(new_table_data)} rows of new data.")
                logger.info(f"File {filename} added to bucket {bucket_name}")

    except InterfaceError:
        logger.error("Error interacting with source database")
    except ClientError as c:
        if c.response["Error"]["Code"] == "ResourceNotFoundException":
            logger.error("Error getting database credentials from Secrets Manager.")
        elif c.response["Error"]["Code"] == "NoSuchBucket":
            logger.error("Error writing file to ingested bucket.")


def get_db_credentials():
    secret_name = "totesys_db_credentials"
    region_name = "eu-west-2"

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager",
                            region_name=region_name)

    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name)


    secret = json.loads(get_secret_value_response["SecretString"])
    db_credentials = {}
    db_credentials["DB_HOST"] = secret["host"]
    db_credentials["DB_USERNAME"] = secret["username"]
    db_credentials["DB_PASSWORD"] = secret["password"]
    db_credentials["DB_NAME"] = secret["dbname"]

    return db_credentials
