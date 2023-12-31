import os
import pytest

import boto3
from moto import mock_s3

from src.processor.utils.convert_and_dump_parquet import (
    convert_and_dump_parquet, generate_object_key)


class TestGenerateObjectKey:
    def test_generates_file_name_matching_star_schema_tables(self):
        expected = "dim_design/31-10-2023/31-10-2023-152600.parquet"
        result = generate_object_key(
            "design/31-10-2023/31-10-2023-152600.csv"
        )
        assert result == expected

        expected = "fact_sales_order/31-10-2023/31-10-2023-152600.parquet"
        result = generate_object_key(
            "sales_order/31-10-2023/31-10-2023-152600.csv"
        )
        assert result == expected

        expected = "dim_location/31-10-2023/31-10-2023-152600.parquet"
        result = generate_object_key(
            "address/31-10-2023/31-10-2023-152600.csv"
        )
        assert result == expected


class TestDumpParquet:
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

    @pytest.fixture
    def test_data(self):
        return [{"staff_id": 1, "first_name": "Jeremie"}]

    def test_puts_parquet_file_in_bucket(self, s3, test_data, empty_bucket):
        convert_and_dump_parquet(
            "design/31-10-2023/31-10-2023-152600.csv",
            test_data,
            "test_processed_bucket"
        )
        response = s3.list_objects(Bucket="test_processed_bucket")
        filename = response["Contents"][0]["Key"]
        assert filename == "dim_design/31-10-2023/31-10-2023-152600.parquet"

    def test_returns_the_created_file_name(self, test_data, empty_bucket):
        assert convert_and_dump_parquet(
            "design/31-10-2023/31-10-2023-152600.csv",
            test_data,
            "test_processed_bucket"
        ) == "dim_design/31-10-2023/31-10-2023-152600.parquet"

    def test_raises_an_error(self, test_data):
        with pytest.raises(Exception):
            convert_and_dump_parquet(
                "design/31-10-2023/31-10-2023-152600.csv",
                test_data,
                "invalid_bucket")
