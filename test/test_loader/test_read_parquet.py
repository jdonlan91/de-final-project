import os
import pytest

import boto3
from moto import mock_s3

from src.processor.utils.convert_and_dump_parquet import convert_and_dump_parquet  # noqa: E501
from src.loader.utils.read_parquet import read_parquet


class TestReadParquet:
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
            Bucket="test_processed_bucket",
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )

    @pytest.fixture(autouse=True)
    def create_test_parquet_files(self, empty_bucket, s3):
        test_parquet_data = [
            {"staff_id": 1, "first_name": "Jeremie", "last_name": "Franey"},
            {"staff_id": 2, "first_name": "Deron", "last_name": "Beier"},
            {"staff_id": 3, "first_name": "Jeanette", "last_name": "Erdman"},
        ]

        convert_and_dump_parquet(
            filename="staff/31-10-2023/31-10-2023-152600.csv",
            transformed_data=test_parquet_data,
            bucket_name="test_processed_bucket"
        )

        convert_and_dump_parquet(
            filename="staff/31-10-2023/31-10-2023-162600.csv",
            transformed_data=[],
            bucket_name="test_processed_bucket"
        )

    def test_returns_string(self):
        result = read_parquet("dim_staff/31-10-2023/31-10-2023-152600.parquet",
                              "test_processed_bucket")

        assert isinstance(result, str)

    def test_returns_empty_str_if_passed_empty_file(self):
        result = read_parquet("dim_staff/31-10-2023/31-10-2023-162600.parquet",
                              "test_processed_bucket")

        assert result == ""

    def test_returns_contents_of_parquet_file(self):
        expected = """staff_id,first_name,last_name
1,Jeremie,Franey
2,Deron,Beier
3,Jeanette,Erdman
"""

        result = read_parquet("dim_staff/31-10-2023/31-10-2023-152600.parquet",
                              "test_processed_bucket")

        assert result == expected
