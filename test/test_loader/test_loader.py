import os
from src.loader.loader import (lambda_handler,
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