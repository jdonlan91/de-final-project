import os
from src.ingestor.ingestor import (lambda_handler,
                                   get_db_credentials,
                                   log_invocation_time,
                                   get_previous_invocation)
from moto import mock_secretsmanager, mock_s3, mock_logs
import boto3
from botocore.exceptions import ClientError
import json
import pytest
from unittest.mock import patch
from datetime import datetime, timezone
from pg8000.exceptions import InterfaceError


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


@pytest.fixture(scope="function")
def s3():
    with mock_s3():
        yield boto3.client("s3", region_name="eu-west-2")


@pytest.fixture
def empty_bucket(s3):
    s3.create_bucket(
        Bucket="test_ingested_bucket",
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
    )


@pytest.fixture
def table_names():
    return [
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


@patch("src.ingestor.ingestor.get_previous_invocation")
@patch("src.ingestor.ingestor.fetch_new_data")
@patch("src.ingestor.ingestor.fetch_table_names")
@patch("src.ingestor.ingestor.get_db_credentials")
@mock_secretsmanager
def test_lambda_calls_fetch_new_data_for_every_table_in_db(mock_db_creds,
                                                           mock_tables,
                                                           mock_fetch,
                                                           mock_prev_invoc,
                                                           table_names):
    mock_prev_invoc.return_value = None
    mock_tables.return_value = table_names
    mock_db_creds.return_value = {
        "DB_HOST": "test-host",
        "DB_PASSWORD": "test_password",
        "DB_USERNAME": "test-username",
        "DB_NAME": "test_db_name",
    }
    lambda_handler(
        event={
            "timestamp": "2024-11-02T14:20:00Z",
            "bucket_name": "test_ingested_bucket",
        },
        context=None,
    )
    assert mock_fetch.call_count == 11
    for table_name in table_names:
        mock_fetch.assert_any_call(
            table_name,
            datetime(2001, 1, 1, 0, 0),
            {
                "DB_HOST": "test-host",
                "DB_PASSWORD": "test_password",
                "DB_USERNAME": "test-username",
                "DB_NAME": "test_db_name",
            },
        )


@mock_secretsmanager
def test_convert_to_csv_is_not_called_if_no_new_data(empty_bucket):
    conn = boto3.client("secretsmanager", region_name="eu-west-2")
    conn.create_secret(
        Name="totesys_db_credentials",
        SecretString=json.dumps(
            {
                "host": "test-host",
                "password": "test_password",
                "username": "test-username",
                "dbname": "test_db_name",
            }
        ),
    )
    with patch("src.ingestor.ingestor.fetch_new_data") as mock_fetch:
        mock_fetch.return_value = []
        with patch("src.ingestor.ingestor.convert_to_csv") as mock_convert:
            lambda_handler(
                event={
                    "timestamp": "2024-11-02T14:20:00Z",
                    "bucket_name": "test_ingested_bucket",
                },
                context=None,
            )
            assert mock_convert.call_count == 0


@patch("src.ingestor.ingestor.get_previous_invocation")
@patch("src.ingestor.ingestor.fetch_new_data")
@patch("src.ingestor.ingestor.fetch_table_names")
@patch("src.ingestor.ingestor.get_db_credentials")
@patch("src.ingestor.ingestor.convert_to_csv")
@mock_secretsmanager
def test_convert_to_csv_called_correct_number_of_times(mock_convert,
                                                       mock_db_creds,
                                                       mock_tables,
                                                       mock_fetch,
                                                       mock_prev_invoc,
                                                       table_names):
    mock_db_creds.return_value = {
        "DB_HOST": "test-host",
        "DB_PASSWORD": "test_password",
        "DB_USERNAME": "test-username",
        "DB_NAME": "test_db_name"
    }
    mock_prev_invoc.return_value = None
    mock_tables.return_value = table_names
    mock_fetch.side_effect = [
        [{"staff_id": 1, "first_name": "Jeremie"}],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
    ]
    mock_convert.return_value = ""
    lambda_handler(
        event={
            "timestamp": "2024-11-02T14:20:00Z",
            "bucket_name": "test_ingested_bucket",
        },
        context=None,
    )
    assert mock_convert.call_count == 1
    mock_convert.assert_any_call(
        [{"staff_id": 1, "first_name": "Jeremie"}])


@patch("src.ingestor.ingestor.get_previous_invocation")
@patch("src.ingestor.ingestor.fetch_new_data")
@patch("src.ingestor.ingestor.fetch_table_names")
@patch("src.ingestor.ingestor.get_db_credentials")
@patch("src.ingestor.ingestor.convert_to_csv")
@patch("src.ingestor.ingestor.dump_data")
@mock_secretsmanager
def test_dump_data_is_invoked_correct_number_of_times(mock_dump,
                                                      mock_convert,
                                                      mock_db_creds,
                                                      mock_tables,
                                                      mock_fetch,
                                                      mock_prev_invoc,
                                                      table_names):
    mock_db_creds.return_value = {
        "DB_HOST": "test-host",
        "DB_PASSWORD": "test_password",
        "DB_USERNAME": "test-username",
        "DB_NAME": "test_db_name"
    }
    mock_prev_invoc.return_value = None
    mock_fetch.return_value = [{"staff_id": 1, "first_name": "Jeremie"}]
    mock_convert.return_value = "staff_id,first_name\n1,Jeremie\n"
    mock_tables.return_value = table_names
    lambda_handler(
        event={
            "timestamp": "2024-11-02T14:20:00Z",
            "bucket_name": "test_ingested_bucket",
        },
        context=None,
    )
    assert mock_dump.call_count == 11
    for table_name in table_names:
        mock_dump.assert_any_call(
            table_name,
            datetime(2024, 11, 2, 14, 20, tzinfo=timezone.utc),
            "staff_id,first_name\n1,Jeremie\n",
            "test_ingested_bucket",
        )


@patch("src.ingestor.ingestor.logger.info")
@patch("src.ingestor.ingestor.get_previous_invocation")
@patch("src.ingestor.ingestor.fetch_new_data")
@patch("src.ingestor.ingestor.fetch_table_names")
@patch("src.ingestor.ingestor.get_db_credentials")
def test_logs_correct_messages_when_no_new_data_is_found(mock_db_creds,
                                                         mock_tables,
                                                         mock_fetch,
                                                         mock_prev_invoc,
                                                         mock_logger,
                                                         table_names):
    mock_db_creds.return_value = {
        "DB_HOST": "test-host",
        "DB_PASSWORD": "test_password",
        "DB_USERNAME": "test-username",
        "DB_NAME": "test_db_name"
    }
    mock_prev_invoc.return_value = None
    mock_fetch.return_value = []
    mock_tables.return_value = table_names
    lambda_handler(
        event={
            "timestamp": "2024-11-02T14:20:00Z",
            "bucket_name": "test_ingested_bucket",
        },
        context=None,
    )
    assert mock_logger.call_count == 22
    for table_name in table_names:
        mock_logger.assert_any_call(f"Table name: {table_name}.")
    mock_logger.assert_any_call("No new data found.")


@patch("src.ingestor.ingestor.logger.info")
@patch("src.ingestor.ingestor.get_previous_invocation")
@patch("src.ingestor.ingestor.fetch_new_data")
@patch("src.ingestor.ingestor.fetch_table_names")
@patch("src.ingestor.ingestor.get_db_credentials")
def test_logs_correct_messages_when_each_table_has_new_data(mock_db_creds,
                                                            mock_tables,
                                                            mock_fetch,
                                                            mock_prev_invoc,
                                                            mock_logger,
                                                            table_names,
                                                            empty_bucket):
    mock_db_creds.return_value = {
        "DB_HOST": "test-host",
        "DB_PASSWORD": "test_password",
        "DB_USERNAME": "test-username",
        "DB_NAME": "test_db_name"
    }
    mock_prev_invoc.return_value = None
    mock_fetch.return_value = [{"staff_id": 1, "first_name": "Jeremie"}]
    mock_tables.return_value = table_names
    lambda_handler(
        event={
            "timestamp": "2024-11-02T14:20:00Z",
            "bucket_name": "test_ingested_bucket",
        },
        context=None,
    )
    assert mock_logger.call_count == 33
    print(mock_logger.mock_calls)
    for t in table_names:
        s = (f"File {t}/02-11-2024/02-11-2024-142000.csv "
             "added to bucket test_ingested_bucket")
        mock_logger.assert_any_call(f"Table name: {t}.")
        mock_logger.assert_any_call("Fetched 1 rows of new data.")
        mock_logger.assert_any_call(s)


@patch("src.ingestor.ingestor.logger.error")
@patch("src.ingestor.ingestor.get_previous_invocation")
@patch("src.ingestor.ingestor.fetch_new_data")
@patch("src.ingestor.ingestor.fetch_table_names")
@patch("src.ingestor.ingestor.get_db_credentials")
def test_when_error_with_source_db_logs_correct_error_message(mock_db_creds,
                                                              mock_tables,
                                                              mock_fetch,
                                                              mock_prev_invoc,
                                                              mock_logger,
                                                              table_names,
                                                              empty_bucket):
    mock_db_creds.return_value = {
        "DB_HOST": "test-host",
        "DB_PASSWORD": "test_password",
        "DB_USERNAME": "test-username",
        "DB_NAME": "test_db_name"
    }
    mock_prev_invoc.return_value = None
    mock_tables.return_value = table_names
    mock_fetch.side_effect = InterfaceError
    lambda_handler(
        event={
            "timestamp": "2024-11-02T14:20:00Z",
            "bucket_name": "test_ingested_bucket",
        },
        context=None,
    )
    mock_logger.assert_called_once_with(
        "Error interacting with source database"
    )


@mock_secretsmanager
def test_when_error_finding_a_secret_logs_correct_error_message():
    conn = boto3.client("secretsmanager", region_name="eu-west-2")
    conn.create_secret(
        Name="invalid_secret",
        SecretString=json.dumps(
            {
                "host": "test-host",
                "password": "test_password",
                "username": "test-username",
                "dbname": "test_db_name",
            }
        ),
    )
    with patch("src.ingestor.ingestor.logger.error") as mock_logger:
        lambda_handler(
            event={
                "timestamp": "2024-11-02T14:20:00Z",
                "bucket_name": "test_ingested_bucket",
            },
            context=None,
        )
        mock_logger.assert_called_once_with(
            "Error getting database credentials from Secrets Manager."
        )


@patch("src.ingestor.ingestor.logger.error")
@patch("src.ingestor.ingestor.get_previous_invocation")
@patch("src.ingestor.ingestor.fetch_new_data")
@patch("src.ingestor.ingestor.fetch_table_names")
@patch("src.ingestor.ingestor.get_db_credentials")
def test_when_error_putting_csv_file_into_bucket_logs_correct_error_message(
    mock_db_creds, mock_tables, mock_fetch, mock_prev_invoc, mock_logger,
    table_names, empty_bucket
):
    mock_db_creds.return_value = {
        "DB_HOST": "test-host",
        "DB_PASSWORD": "test_password",
        "DB_USERNAME": "test-username",
        "DB_NAME": "test_db_name"
    }
    mock_prev_invoc.return_value = None
    mock_fetch.return_value = [{"name": "TestName"}]
    mock_tables.return_value = table_names
    lambda_handler(
        event={
            "timestamp": "2024-11-02T14:20:00Z",
            "bucket_name": "invalid_bucket",
        },
        context=None,
    )
    mock_logger.assert_called_once_with(
        "Error writing file to ingested bucket."
    )


@patch("src.ingestor.ingestor.logger.error")
@patch("src.ingestor.ingestor.dump_data")
@patch("src.ingestor.ingestor.get_previous_invocation")
@patch("src.ingestor.ingestor.fetch_new_data")
@patch("src.ingestor.ingestor.fetch_table_names")
@patch("src.ingestor.ingestor.get_db_credentials")
def test_when_general_client_error_logs_correct_error_message(mock_db_creds,
                                                              mock_tables,
                                                              mock_fetch,
                                                              mock_prev_invoc,
                                                              mock_dump,
                                                              mock_logger,
                                                              table_names,
                                                              empty_bucket):
    mock_db_creds.return_value = {
        "DB_HOST": "test-host",
        "DB_PASSWORD": "test_password",
        "DB_USERNAME": "test-username",
        "DB_NAME": "test_db_name"
    }
    mock_prev_invoc.return_value = None
    mock_fetch.return_value = [{"name": "TestName"}]
    mock_dump.side_effect = ClientError(
        {
            "Error": {
                "Code": "SampleErrorCode",
                "Message": "Example error message",
            }
        },
        "Operation name",
    )
    mock_tables.return_value = table_names
    lambda_handler(
        event={
            "timestamp": "2024-11-02T14:20:00Z",
            "bucket_name": "test_ingested_bucket",
        },
        context=None,
    )
    mock_logger.assert_called_once_with(
        "AWS client error SampleErrorCode.\nExample error message."
    )


@patch("src.ingestor.ingestor.logger.error")
@patch("src.ingestor.ingestor.dump_data")
@patch("src.ingestor.ingestor.get_previous_invocation")
@patch("src.ingestor.ingestor.fetch_new_data")
@patch("src.ingestor.ingestor.fetch_table_names")
@patch("src.ingestor.ingestor.get_db_credentials")
def test_when_general_exception_logs_correct_error_message(mock_db_creds,
                                                           mock_tables,
                                                           mock_fetch,
                                                           mock_prev_invoc,
                                                           mock_dump,
                                                           mock_logger,
                                                           table_names):
    mock_db_creds.return_value = {
        "DB_HOST": "test-host",
        "DB_PASSWORD": "test_password",
        "DB_USERNAME": "test-username",
        "DB_NAME": "test_db_name"
    }
    mock_prev_invoc.return_value = None
    mock_fetch.return_value = [{"name": "TestName"}]
    mock_dump.side_effect = Exception
    mock_tables.return_value = table_names
    lambda_handler(
        event={
            "timestamp": "2024-11-02T14:20:00Z",
            "bucket_name": "test_ingested_bucket",
        },
        context=None,
    )
    mock_logger.assert_any_call("Unexpected error occurred.")


@mock_secretsmanager
def test_get_db_credentials_returns_correct_credentials():
    conn = boto3.client("secretsmanager", region_name="eu-west-2")
    conn.create_secret(
        Name="totesys_db_credentials",
        SecretString=json.dumps(
            {
                "host": "test-host",
                "password": "test_password",
                "username": "test-username",
                "dbname": "test_db_name",
            }
        ),
    )
    db_credentials = get_db_credentials()
    assert db_credentials["DB_HOST"] == "test-host"


@mock_secretsmanager
def test_get_db_credentials_raises_error_when_fails_to_access_secret():
    conn = boto3.client("secretsmanager", region_name="eu-west-2")
    conn.create_secret(
        Name="wrong_db_credentials",
        SecretString=json.dumps(
            {
                "host": "test-host",
                "password": "test_password",
                "username": "test-username",
                "dbname": "test_db_name",
            }
        ),
    )
    with pytest.raises(Exception):
        get_db_credentials()


class TestLogInvocationTime():

    @mock_logs
    def test_logs_invocation_time(self, aws_credentials):
        conn = boto3.client("logs")
        conn.create_log_group(logGroupName="test_log_group")
        conn.create_log_stream(logGroupName="test_log_group",
                               logStreamName="test_log_stream")
        log_invocation_time(datetime.strptime(
            "31-10-2023-152600", "%d-%m-%Y-%H%M%S"),
            "test_log_group", "test_log_stream")
        log_events = conn.get_log_events(
            logGroupName="test_log_group", logStreamName="test_log_stream")

        assert log_events['events'][0]['message'] == "31-10-2023-152600"


class TestGetPreviousInvocation():

    @mock_logs
    def test_returns_previous_invocation(self, aws_credentials):
        conn = boto3.client("logs")
        conn.create_log_group(logGroupName="test_log_group")
        conn.create_log_stream(logGroupName="test_log_group",
                               logStreamName="test_log_stream")
        log_invocation_time(datetime.strptime(
            "31-10-2023-152600", "%d-%m-%Y-%H%M%S"),
            "test_log_group", "test_log_stream")
        prev_invocation = get_previous_invocation(
            "test_log_group", "test_log_stream")

        assert prev_invocation.strftime(
            "%d-%m-%Y-%H%M%S") == "31-10-2023-152600"

    @mock_logs
    def test_if_no_previous_invocation_returns_none(self, aws_credentials):
        conn = boto3.client("logs")
        conn.create_log_group(logGroupName="test_log_group")
        conn.create_log_stream(logGroupName="test_log_group",
                               logStreamName="test_log_stream")
        prev_invocation = get_previous_invocation(
            "test_log_group", "test_log_stream")

        assert prev_invocation is None
