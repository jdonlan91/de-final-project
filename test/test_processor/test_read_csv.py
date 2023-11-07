import os
import pytest
from datetime import datetime

import boto3
from moto import mock_s3

from src.processor.utils.read_csv import read_csv
from src.ingestor.utils.dump_data import dump_data


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
    def create_test_csv_file(self, empty_bucket):
        csv_string = """id,firstname,lastname
                        1,Rosanne,Harriman
                        2,Hermione,Leler
                        3,Bernardine,Cosenza"""

        dump_data("test_table", datetime.strptime("31-10-2023-152600",
                                                  "%d-%m-%Y-%H%M%S"), csv_string, "test_ingested_bucket")

    def test_returns_list_of_dictionaries(self, create_test_csv_file):
        result = read_csv(
            "test_table/31-10-2023/31-10-2023-152600.csv",
            "test_ingested_bucket")
        assert isinstance(result, list)

        for item in result:
            assert isinstance(item, dict)

    def test_returns_empty_list_if_passed_file_with_no_data(self):
        pass

    def test_returns_contents_of_csv_as_list_of_dictionaries(self):
        pass
