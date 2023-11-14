import os
import pytest
from datetime import datetime
from dateutil.tz import tzutc
from unittest.mock import patch

import boto3
from moto import mock_s3

from src.loader.utils.fetch_new_files import (fetch_new_files, sort_new_files)
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
            filename="staff/02-11-2024/02-11-2024-142200.csv",
            transformed_data=[],
            bucket_name="test_processed_bucket"
        )

        convert_and_dump_parquet(
            filename="staff/02-11-2024/02-11-2024-142300.csv",
            transformed_data=[],
            bucket_name="test_processed_bucket"
        )

        convert_and_dump_parquet(
            filename="staff/02-11-2024/02-11-2024-142400.csv",
            transformed_data=[],
            bucket_name="test_processed_bucket"
        )

        convert_and_dump_parquet(
            filename="staff/02-11-2024/02-11-2024-142500.csv",
            transformed_data=[],
            bucket_name="test_processed_bucket"
        )

    def test_returns_a_list_of_strings(self):
        result = fetch_new_files(
            "test_processed_bucket",
            datetime.strptime(
                "02-11-2024-142552", "%d-%m-%Y-%H%M%S")
        )
        assert isinstance(result, list)

        for item in result:
            assert isinstance(item, str)

    @patch("src.loader.utils.fetch_new_files.get_all_file_names")
    def test_returns_a_list_of_files_more_recent_than_timestamp(self,
                                                                mock_get_all):
        expected = [
            "dim_staff/02-11-2024/02-11-2024-142400.parquet",
            "dim_staff/02-11-2024/02-11-2024-142500.parquet"
        ]

        mock_get_all.return_value = {
            'Contents':
            [{'Key': 'dim_staff/02-11-2024/02-11-2024-142200.parquet',
              'LastModified': datetime(2024, 11, 2, 14, 22, 0, tzinfo=tzutc())
              },
             {'Key': 'dim_staff/02-11-2024/02-11-2024-142300.parquet',
              'LastModified': datetime(2024, 11, 2, 14, 23, 0, tzinfo=tzutc())
              },
             {'Key': 'dim_staff/02-11-2024/02-11-2024-142400.parquet',
              'LastModified': datetime(2024, 11, 2, 14, 24, 0, tzinfo=tzutc())
              },
             {'Key': 'dim_staff/02-11-2024/02-11-2024-142500.parquet',
              'LastModified': datetime(2024, 11, 2, 14, 25, 0, tzinfo=tzutc())
              }]
        }

        result = fetch_new_files(
            "test_processed_bucket",
            datetime.strptime(
                "02-11-2024-142330", "%d-%m-%Y-%H%M%S")
        )
        assert result == expected

    @patch("src.loader.utils.fetch_new_files.get_all_file_names")
    def test_if_no_new_files_returns_empty_list(self, mock_get_all):
        mock_get_all.return_value = {
            'Contents':
            [{'Key': 'dim_staff/02-11-2024/02-11-2024-142200.parquet',
              'LastModified': datetime(2024, 11, 2, 14, 22, 0, tzinfo=tzutc())
              },
             {'Key': 'dim_staff/02-11-2024/02-11-2024-142300.parquet',
              'LastModified': datetime(2024, 11, 2, 14, 23, 0, tzinfo=tzutc())
              },
             {'Key': 'dim_staff/02-11-2024/02-11-2024-142400.parquet',
              'LastModified': datetime(2024, 11, 2, 14, 24, 0, tzinfo=tzutc())
              },
             {'Key': 'dim_staff/02-11-2024/02-11-2024-142500.parquet',
              'LastModified': datetime(2024, 11, 2, 14, 25, 0, tzinfo=tzutc())
              }]
        }

        result = fetch_new_files(
            "test_processed_bucket",
            datetime.strptime(
                "02-11-2024-142630", "%d-%m-%Y-%H%M%S")
        )
        assert result == []


class TestSortNewFiles:
    def test_sorts_by_timestamp(self):
        unsorted_file_names = [
            'dim_staff/02-11-2024/02-11-2024-142500.parquet',
            'dim_staff/02-11-2024/02-11-2024-132500.parquet',
            'dim_staff/02-11-2024/02-11-2024-152500.parquet',
            'dim_staff/02-11-2024/02-11-2024-102500.parquet'
        ]

        expected = [
            'dim_staff/02-11-2024/02-11-2024-102500.parquet',
            'dim_staff/02-11-2024/02-11-2024-132500.parquet',
            'dim_staff/02-11-2024/02-11-2024-142500.parquet',
            'dim_staff/02-11-2024/02-11-2024-152500.parquet'
        ]

        assert sort_new_files(unsorted_file_names) == expected

    def test_if_same_timestamp_sorts_by_table_name(self):
        unsorted_file_names = [
            'dim_staff/02-11-2024/02-11-2024-142500.parquet',
            'fact_sales_order/02-11-2024/02-11-2024-142500.parquet',
            'dim_design/02-11-2024/02-11-2024-142500.parquet',
            'fact_sales_order/02-11-2024/02-11-2024-140000.parquet'
        ]

        expected = [
            'fact_sales_order/02-11-2024/02-11-2024-140000.parquet',
            'dim_design/02-11-2024/02-11-2024-142500.parquet',
            'dim_staff/02-11-2024/02-11-2024-142500.parquet',
            'fact_sales_order/02-11-2024/02-11-2024-142500.parquet'
        ]

        assert sort_new_files(unsorted_file_names) == expected
