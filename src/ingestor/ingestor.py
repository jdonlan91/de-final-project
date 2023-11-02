# Dependencies: pg8000

# Arguments: N/A

# This will call fetch_new_data on each table in a database.

# If fetch_new_data returns new table data, it will pass the data to convert_to_csv, and then to dump_data, which will dump csv data packets into ingestion bucket.

# If fetch new data returns an empty list, the ingestor lambda returns without taking any further actions.

# Logs:

# name of table
# name of CSV file
# number of new rows

from datetime import datetime
from utils.convert_to_csv import convert_to_csv
from utils.dump_data import dump_data
from utils.fetch_new_data import fetch_new_data
import logging

logger = logging.getLogger('Ingestor logger')
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

        # get credentials from AWS Secrets Manager

        table_names = ['sales_order', 'design', 'currency', 'staff', 'counterparty',
                       'address', 'department', 'purchase_order', 'payment_type', 'payment', 'transaction']

        timestamp = datetime.now()

        # get bucket name from event metadata

        for table_name in table_names:
            new_table_data = fetch_new_data(
                table_name, timestamp, db_credentials)
            logger.info(f'Table name: {table_name}.')
            if len(new_table_data) == 0:
                logger.info(f'No new data found.')
                continue
            else:
                csv_string = convert_to_csv(new_table_data)
                filename = dump_data(table_name, timestamp,
                                     csv_string, bucket_name)
                logger.info(f'Fetched {len(new_table_data)} rows of new data.')
                logger.info(
                    f'New file {filename} created in S3 bucket {bucket_name}')

    except Exception as e:
        raise e
