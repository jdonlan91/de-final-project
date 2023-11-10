import os
import pytest

import boto3
from moto import mock_s3

from src.loader.utils.fetch_new_files import fetch_new_files
from src.processor.utils.convert_and_dump_parquet import convert_and_dump_parquet  # noqa: E501


class TestFetchNewFile:
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
    def create_test_files(self, empty_bucket, s3):
        convert_and_dump_parquet(
            filename="02-11-2024-142200.parquet",
            transformed_data=[],
            bucket_name="test_processed_bucket"
        )

        convert_and_dump_parquet(
            filename="02-11-2024-142300.parquet",
            transformed_data=[],
            bucket_name="test_processed_bucket"
        )

        convert_and_dump_parquet(
            filename="02-11-2024-142400.parquet",
            transformed_data=[],
            bucket_name="test_processed_bucket"
        )

        convert_and_dump_parquet(
            filename="02-11-2024-142500.parquet",
            transformed_data=[],
            bucket_name="test_processed_bucket"
        )

    def test_returns_a_list_of_strings(self):
        result = fetch_new_files(
            "test_processed_bucket",
            "2024-11-02 14:25:52.186"
        )
        assert isinstance(result, list)

        for item in result:
            assert isinstance(item, str)

    def test_returns_an_empty_list_if_no_new_files_found(self):
        result = fetch_new_files(
            "test_processed_bucket",
            "2024-11-02 14:20:52.186"
        )
        assert result == []

    def test_returns_a_list_of_unloaded_files(self):
        expected = [
            "01-11-2024-142200.parquet",
            "01-11-2024-142300.parquet",
            "02-11-2024-142400.parquet",
            "02-11-2024-142500.parquet"
        ]
        result = fetch_new_files(
            "test_processed_bucket",
            "2024-11-02 14:25:52.186"
        )
        assert result == expected

    def test_ignores_files_loaded_before_invocation_time(self):
        expected = [
            "02-11-2024-142400.parquet",
            "02-11-2024-142500.parquet"
        ]
        result = fetch_new_files(
            "test_processed_bucket",
            "2024-11-02 14:28:52.186"
        )
        assert result == expected
