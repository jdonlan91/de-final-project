import os
import pytest

import boto3
from moto import mock_s3

from src.processor.utils.read_csv import read_csv


class TestReadCsv:
    @pytest.fixture(scope="function")
    def aws_credentials(self):
        """Mocked AWS Credentials for moto."""

        os.environ["AWS_ACCESS_KEY_ID"] = "test"
        os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
        os.environ["AWS_SECURITY_TOKEN"] = "test"
        os.environ["AWS_SESSION_TOKEN"] = "test"
        os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"

    @pytest.fixture(scope="function")
    def s3(self, aws_credentials):
        with mock_s3():
            yield boto3.client("s3", region_name="eu-west-2")

    @pytest.fixture
    def empty_bucket(self, s3):
        s3.create_bucket(
            Bucket="test_ingested_bucket",
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )

    @pytest.fixture(autouse=True)
    def create_test_csv_files(self, empty_bucket, s3):
        test_csv_data = """id|firstname|lastname
                        1|Rosanne|Harriman
                        2|Hermione|Leler
                        3|Bernardine|Cosenza"""

        s3.put_object(
            Body=test_csv_data,
            Bucket="test_ingested_bucket",
            Key="test_folder/test_file.csv"
        )

        s3.put_object(
            Body="",
            Bucket="test_ingested_bucket",
            Key="test_folder/test_empty_file.csv"
        )

    def test_returns_list_of_dictionaries(self):
        result = read_csv(
            "test_folder/test_file.csv",
            "test_ingested_bucket")

        assert isinstance(result, list)

        for item in result:
            assert isinstance(item, dict)

    def test_returns_empty_list_if_passed_file_with_no_data(self):
        result = read_csv(
            "test_folder/test_empty_file.csv",
            "test_ingested_bucket")

        assert result == []

    def test_returns_contents_of_csv_as_list_of_dictionaries(self):
        expected = [
            {'id': '1', 'firstname': 'Rosanne', 'lastname': 'Harriman'},
            {'id': '2', 'firstname': 'Hermione', 'lastname': 'Leler'},
            {'id': '3', 'firstname': 'Bernardine', 'lastname': 'Cosenza'}
        ]

        result = read_csv(
            "test_folder/test_file.csv",
            "test_ingested_bucket")

        assert result == expected
