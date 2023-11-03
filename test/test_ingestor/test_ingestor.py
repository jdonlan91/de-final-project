from src.ingestor.ingestor import lambda_handler, get_db_credentials
from moto import mock_secretsmanager, mock_s3
import boto3
from botocore.exceptions import ClientError
import json
import pytest
from unittest.mock import patch
from datetime import datetime, timezone


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


@mock_secretsmanager
def test_lambda_calls_fetch_new_data_for_every_table_in_db(empty_bucket):
    conn = boto3.client("secretsmanager", region_name="eu-west-2")
    conn.create_secret(
        Name="totesys_db_credentials",
        SecretString=json.dumps(
            {
                "host": "test-host",
                "password": "test_password",
                "username": "test-username",
                "dbname": "test_db_name"
            }
        )
    )
    with patch("src.ingestor.ingestor.fetch_new_data") as mock_fetch:
        lambda_handler(
            event={
                "timestamp": "2024-11-02T14:20:00Z",
                "bucket_name": "test_ingested_bucket"
            },
            context=None
        )
        assert mock_fetch.call_count == 11
        print(mock_fetch.mock_calls)
        mock_fetch.assert_any_call(
            "sales_order",
            datetime(2024, 11, 2, 14, 15, tzinfo=timezone.utc),
            {
                "DB_HOST": "test-host",
                "DB_PASSWORD": "test_password",
                "DB_USERNAME": "test-username",
                "DB_NAME": "test_db_name"
            }
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


@mock_secretsmanager
def test_convert_to_csv_called_correct_number_of_times(empty_bucket):
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
        with patch("src.ingestor.ingestor.convert_to_csv") as mock_convert:
            mock_convert.return_value = ""
            lambda_handler(
                event={
                    "timestamp": "2024-11-02T14:20:00Z",
                    "bucket_name": "test_ingested_bucket",
                },
                context=None,
            )
            assert mock_convert.call_count == 1
            mock_convert.assert_any_call([
                {"staff_id": 1, "first_name": "Jeremie"}
                ])


@mock_secretsmanager
def test_dump_data(empty_bucket):
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
        mock_fetch.return_value = [{"staff_id": 1, "first_name": "Jeremie"}]
        with patch("src.ingestor.ingestor.convert_to_csv") as mock_convert:
            mock_convert.return_value = "staff_id,first_name\n1,Jeremie\n"
            with patch("src.ingestor.ingestor.dump_data") as mock_dump:
                lambda_handler(
                    event={
                        "timestamp": "2024-11-02T14:20:00Z",
                        "bucket_name": "test_ingested_bucket",
                    },
                    context=None,
                )
                assert mock_dump.call_count == 11
                print(mock_dump.mock_calls)
                mock_dump.assert_any_call(
                    "sales_order",
                    datetime(2024, 11, 2, 14, 15, tzinfo=timezone.utc),
                    "staff_id,first_name\n1,Jeremie\n",
                    "test_ingested_bucket",
                )


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
    with pytest.raises(ClientError):
        get_db_credentials()
