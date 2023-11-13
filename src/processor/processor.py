import logging
import os

from botocore.exceptions import ClientError
from pg8000.exceptions import InterfaceError

from utils.read_csv import read_csv
from utils.transform_data import transform_data
from utils.convert_and_dump_parquet import (
    convert_and_dump_parquet)


logger = logging.getLogger("Ingestor logger")
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """
    Takes data from ingested bucket, transforms and converts the data
    into parquet and dumps the data into processed bucket.

    Triggered by s3:CreateObject when a new file is dumped into
    the ingested bucket.

    Calls read_csv util function to read ingested data.
    Calls transform_data util function to transform data into relevant schema.
    Calls convert_and_dump_parquet util function to dump parquet files
    into processed bucket.
    Logs metadata about files added to the processed bucket.
    Logs any errors that occur.



    """
    try:
        filename = event["Records"][0]["s3"]["object"]["key"]
        read_bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
        dump_bucket_name = os.environ["PROCESSED_BUCKET_NAME"]

        data_to_transform = read_csv(filename, read_bucket_name)
        transformed_data = transform_data(filename, data_to_transform)
        if transformed_data is not None:
            new_filename = convert_and_dump_parquet(filename,
                                                    transformed_data,
                                                    dump_bucket_name)

            logger.info(
                f"File {new_filename} added to bucket {dump_bucket_name}")

    except InterfaceError:
        logger.error("Error interacting with database.")
    except ClientError as c:
        if c.response["Error"]["Code"] == "ResourceNotFoundException":
            logger.error(
                "Error getting database credentials from Secrets Manager.")
        elif c.response["Error"]["Code"] == "NoSuchBucket":
            logger.error("Error acessing the bucket. NoSuchBucket.")
        else:
            logger.error(
                f"""AWS client error {c.response['Error']['Code']}.
{c.response['Error']['Message']}."""
            )
    except Exception as e:
        logger.error("Unexpected error occurred.")
        logger.error(e)
