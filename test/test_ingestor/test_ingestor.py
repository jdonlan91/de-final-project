from src.ingestor.ingestor import lambda_handler, get_db_credentials
from moto import mock_secretsmanager, mock_s3
import boto3
from botocore.exceptions import ClientError
import json
import pytest


@mock_secretsmanager
def test_get_db_credentials_returns_correct_credentials():
    conn = boto3.client("secretsmanager", region_name="eu-west-2")
    put_secret_value_dict = conn.create_secret(
        Name="totesys_db_credentials",
        SecretString=json.dumps({'host': 'test-host', 'password': 'test_password', 'username': 'test-username', 'dbname': 'test_db_name'}),
    )
    db_credentials = get_db_credentials()
    assert db_credentials['DB_HOST'] == 'test-host'


@mock_secretsmanager
def test_get_db_credentials_raises_error_when_fails_to_access_secret():
    conn = boto3.client("secretsmanager", region_name="eu-west-2")
    put_secret_value_dict = conn.create_secret(
        Name="wrong_db_credentials",
        SecretString=json.dumps({'host': 'test-host', 'password': 'test_password', 'username': 'test-username', 'dbname': 'test_db_name'}),
    )
    with pytest.raises(ClientError):
        get_db_credentials()