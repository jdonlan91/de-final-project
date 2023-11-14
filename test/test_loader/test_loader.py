from datetime import datetime
import json
import os
import pytest

import boto3
from botocore.exceptions import ClientError
from moto import mock_secretsmanager, mock_s3, mock_logs
from pg8000.exceptions import InterfaceError
from unittest.mock import patch

from src.loader.loader import (
    lambda_handler,
    get_db_credentials,
    log_invocation_time,
    get_previous_invocation
)


@pytest.fixture(autouse=True)
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


@pytest.fixture
def test_event():
    return {
        "timestamp": "2024-11-02T14:20:00Z",
        "bucket_name": "test_processed_bucket",
    }


@pytest.fixture
def test_db_credentials():
    return {
        "DB_HOST": "test-host",
        "DB_PASSWORD": "test_password",
        "DB_USERNAME": "test-username",
        "DB_NAME": "test_db_name",
    }


@pytest.fixture
def s3():
    with mock_s3():
        yield boto3.client("s3", region_name="eu-west-2")


@pytest.fixture
def empty_bucket(s3):
    s3.create_bucket(
        Bucket="test_processed_bucket",
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
    )


class TestSeedDimDate:
    @patch("src.loader.loader.log_invocation_time")
    @patch("src.loader.loader.fetch_new_files")
    @patch("src.loader.loader.seed_dim_date")
    @patch("src.loader.loader.get_previous_invocation")
    @patch("src.loader.loader.get_db_credentials")
    @mock_secretsmanager
    def test_seed_dim_date_is_called_on_first_invocation(
        self,
        mock_get_db_credentials,
        mock_prev_invoc,
        mock_seed,
        mock_fetch,
        mock_log,
        test_event,
        test_db_credentials,
        empty_bucket
    ):
        mock_get_db_credentials.return_value = test_db_credentials
        mock_prev_invoc.return_value = None
        mock_fetch.return_value = []
        lambda_handler(event=test_event, context=None)
        mock_seed.assert_called_once_with(test_db_credentials)

    @patch("src.loader.loader.log_invocation_time")
    @patch("src.loader.loader.populate_schema")
    @patch("src.loader.loader.read_parquet")
    @patch("src.loader.loader.fetch_new_files")
    @patch("src.loader.utils.seed_dim_date")
    @patch("src.loader.loader.get_previous_invocation")
    @patch("src.loader.loader.get_db_credentials")
    @mock_secretsmanager
    def test_seed_dim_date_is_not_called_if_not_first_invocation(
        self,
        mock_get_db_credentials,
        mock_prev_invoc,
        mock_seed,
        mock_fetch,
        mock_read,
        mock_populate,
        mock_log,
        test_event
    ):
        mock_get_db_credentials.return_value = test_db_credentials
        mock_prev_invoc.return_value = "31-10-2023-152600"
        mock_fetch.return_value = ["test-file-name"]

        lambda_handler(event=test_event, context=None)

        assert mock_seed.call_count == 0


class TestUtilFunctionInvocations:
    @patch("src.loader.loader.logger")
    @patch("src.loader.loader.log_invocation_time")
    @patch("src.loader.loader.populate_schema")
    @patch("src.loader.loader.read_parquet")
    @patch("src.loader.loader.fetch_new_files")
    @patch("src.loader.utils.seed_dim_date")
    @patch("src.loader.loader.get_previous_invocation")
    @patch("src.loader.loader.get_db_credentials")
    @mock_secretsmanager
    def test_fetch_new_files_called_with_correct_arguments(
        self,
        mock_get_db_credentials,
        mock_prev_invoc,
        mock_seed,
        mock_fetch,
        mock_read,
        mock_populate,
        mock_log,
        mock_logger,
        test_event
    ):
        mock_get_db_credentials.return_value = test_db_credentials
        mock_prev_invoc.return_value = "31-10-2023-152600"
        mock_fetch.return_value = []

        lambda_handler(event=test_event, context=None)
        mock_fetch.assert_any_call(
            "test_processed_bucket",
            "31-10-2023-152600"
        )
        mock_logger.info.assert_called_once_with("No new files.")

    @patch("src.loader.loader.logger")
    @patch("src.loader.loader.log_invocation_time")
    @patch("src.loader.loader.populate_schema")
    @patch("src.loader.loader.read_parquet")
    @patch("src.loader.loader.fetch_new_files")
    @patch("src.loader.utils.seed_dim_date")
    @patch("src.loader.loader.get_previous_invocation")
    @patch("src.loader.loader.get_db_credentials")
    @mock_secretsmanager
    def test_if_fetch_new_files_returns_empty_list_correct_msg_logged_and_execution_stops(  # noqa: E501
        self,
        mock_get_db_credentials,
        mock_prev_invoc,
        mock_seed,
        mock_fetch,
        mock_read,
        mock_populate,
        mock_log,
        mock_logger,
        test_event
    ):
        mock_get_db_credentials.return_value = test_db_credentials
        mock_prev_invoc.return_value = "31-10-2023-152600"
        mock_fetch.return_value = []
        lambda_handler(event=test_event, context=None)
        mock_logger.info.assert_called_once_with("No new files.")
        assert mock_read.call_count == 0
        assert mock_populate.call_count == 0

    @patch("src.loader.loader.logger")
    @patch("src.loader.loader.log_invocation_time")
    @patch("src.loader.loader.populate_schema")
    @patch("src.loader.loader.read_parquet")
    @patch("src.loader.loader.fetch_new_files")
    @patch("src.loader.utils.seed_dim_date")
    @patch("src.loader.loader.get_previous_invocation")
    @patch("src.loader.loader.get_db_credentials")
    @mock_secretsmanager
    def test_if_fetch_new_files_returns_new_files_read_parquet_and_populate_schema_called_correctly(  # noqa: E501
        self,
        mock_get_db_credentials,
        mock_prev_invoc,
        mock_seed,
        mock_fetch,
        mock_read,
        mock_populate,
        mock_log,
        mock_logger,
        test_event
    ):
        mock_get_db_credentials.return_value = test_db_credentials
        mock_prev_invoc.return_value = "31-10-2023-152600"
        mock_fetch.return_value = ["test-file-one", "test-file-two"]
        mock_read.return_value = "test-csv-string"
        mock_populate.side_effect = [
            "File test-file-one loaded.",
            "File test-file-two loaded."
        ]

        lambda_handler(event=test_event, context=None)
        assert mock_read.call_count == 2
        mock_read.assert_any_call("test-file-one", "test_processed_bucket")
        mock_read.assert_any_call("test-file-two", "test_processed_bucket")
        assert mock_populate.call_count == 2
        mock_populate.assert_any_call(
            test_db_credentials,
            "test-file-one",
            "test-csv-string"
        )
        mock_populate.assert_any_call(
            test_db_credentials,
            "test-file-two",
            "test-csv-string"
        )
        assert mock_logger.info.call_count == 2
        mock_logger.info.assert_any_call("File test-file-one loaded.")
        mock_logger.info.assert_any_call("File test-file-two loaded.")


@mock_secretsmanager
class TestGetDbCredentials:
    def test_get_db_credentials_returns_correct_credentials(self):
        conn = boto3.client("secretsmanager", region_name="eu-west-2")
        conn.create_secret(
            Name="postgres_db_credentials",
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

    def test_get_db_credentials_raises_error_when_fails_to_access_secret(self):
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
    def test_logs_invocation_time(self):
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
    def test_returns_previous_invocation(self):
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
    def test_if_no_previous_invocation_returns_none(self):
        conn = boto3.client("logs")
        conn.create_log_group(logGroupName="test_log_group")
        conn.create_log_stream(logGroupName="test_log_group",
                               logStreamName="test_log_stream")
        prev_invocation = get_previous_invocation(
            "test_log_group", "test_log_stream")

        assert prev_invocation is None


@patch("src.loader.loader.logger")
@patch("src.loader.loader.log_invocation_time")
@patch("src.loader.loader.populate_schema")
@patch("src.loader.loader.read_parquet")
@patch("src.loader.loader.fetch_new_files")
@patch("src.loader.utils.seed_dim_date")
@patch("src.loader.loader.get_previous_invocation")
@patch("src.loader.loader.get_db_credentials")
class TestErrorLogging:
    def test_when_error_with_source_db_logs_correct_error_message(
        self,
        mock_get_db_credentials,
        mock_prev_invoc,
        mock_seed,
        mock_fetch,
        mock_read,
        mock_populate,
        mock_log,
        mock_logger,
        test_event
    ):
        mock_get_db_credentials.return_value = test_db_credentials
        mock_prev_invoc.return_value = "31-10-2023-152600"
        mock_fetch.return_value = ["test-file-one", "test-file-two"]
        mock_read.return_value = "test-csv-string"
        mock_populate.side_effect = InterfaceError
        lambda_handler(event=test_event, context=None)

        mock_logger.error.assert_called_once_with(
            "Error interacting with database.")

    def test_when_error_finding_a_secret_logs_correct_error_message(
        self,
        mock_get_db_credentials,
        mock_prev_invoc,
        mock_seed,
        mock_fetch,
        mock_read,
        mock_populate,
        mock_log,
        mock_logger,
        test_event
    ):
        mock_get_db_credentials.side_effect = ClientError(
            {
                "Error": {
                    "Code": "ResourceNotFoundException",
                }
            },
            "Operation name",
        )

        lambda_handler(event=test_event, context=None)

        mock_logger.error.assert_called_once_with(
            "Error getting database credentials from Secrets Manager."
        )

    def test_when_error_accessing_a_bucket_logs_correct_error_message(
        self,
        mock_get_db_credentials,
        mock_prev_invoc,
        mock_seed,
        mock_fetch,
        mock_read,
        mock_populate,
        mock_log,
        mock_logger,
        test_event
    ):
        mock_get_db_credentials.return_value = test_db_credentials
        mock_prev_invoc.return_value = "31-10-2023-152600"
        mock_fetch.side_effect = ClientError(
            {
                "Error": {
                    "Code": "NoSuchBucket",
                }
            },
            "Operation name",
        )

        lambda_handler(event=test_event, context=None)

        mock_logger.error.assert_called_once_with(
            "Error acessing the bucket. NoSuchBucket."
        )

    def test_when_general_aws_error_logs_correct_error_message(
        self,
        mock_get_db_credentials,
        mock_prev_invoc,
        mock_seed,
        mock_fetch,
        mock_read,
        mock_populate,
        mock_log,
        mock_logger,
        test_event
    ):
        mock_get_db_credentials.return_value = test_db_credentials
        mock_prev_invoc.side_effect = ClientError(
            {
                "Error": {
                    "Code": "SampleErrorCode",
                    "Message": "Example error message",
                }
            },
            "Operation name",
        )

        lambda_handler(event=test_event, context=None)

        mock_logger.error.assert_called_once_with(
            "AWS client error SampleErrorCode.\nExample error message."
        )

    def test_when_general_exception_logs_correct_error_message(
        self,
        mock_get_db_credentials,
        mock_prev_invoc,
        mock_seed,
        mock_fetch,
        mock_read,
        mock_populate,
        mock_log,
        mock_logger,
        test_event
    ):
        mock_get_db_credentials.return_value = test_db_credentials
        mock_prev_invoc.return_value = "31-10-2023-152600"
        mock_fetch.side_effect = Exception

        lambda_handler(event=test_event, context=None)

        mock_logger.error.assert_any_call("Unexpected error occurred.")
