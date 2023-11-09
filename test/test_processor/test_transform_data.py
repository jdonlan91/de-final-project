import json
import pytest

import boto3
from moto import mock_secretsmanager
from pg8000.exceptions import InterfaceError
from unittest.mock import patch

from src.processor.utils.transform_data import (
    get_db_credentials,
    create_connection,
    query_database,
    transform_counterparty,
    transform_staff,
    transform_sales_order,
    # transform_data
)

from fixtures.transform_counterparty_data import test_counterparty_data  # noqa: F401
from fixtures.transform_staff_data import test_staff_data  # noqa: F401
from fixtures.transform_sales_data import test_sales_data  # noqa: F401


class TestGetDbCredentials:
    @mock_secretsmanager
    def test_get_db_credentials_returns_correct_credentials(self):
        conn = boto3.client("secretsmanager", region_name="eu-west-2")
        conn.create_secret(
            Name="totesys_db_credentials",
            SecretString=json.dumps(
                {
                    "host": "test-host",
                    "password": "test_password",
                    "username": "test_username",
                    "dbname": "test_db_name",
                }
            ),
        )
        db_credentials = get_db_credentials()
        assert db_credentials["DB_HOST"] == "test-host"

    @mock_secretsmanager
    def test_get_db_credentials_raises_error_when_fails_to_access_secret(self):
        conn = boto3.client("secretsmanager", region_name="eu-west-2")
        conn.create_secret(
            Name="wrong_db_credentials",
            SecretString=json.dumps(
                {
                    "host": "test-host",
                    "password": "test_password",
                    "username": "test_username",
                    "dbname": "test_db_name",
                }
            ),
        )
        with pytest.raises(Exception):
            get_db_credentials()


class TestCreateConnection:
    def test_create_connection_failure(self):
        db_credentials = {
            "DB_USERNAME": "invalid_user",
            "DB_PASSWORD": "invalid_password",
            "DB_HOST": "invalid_host",
            "DB_NAME": "invalid_db",
        }

        with pytest.raises(InterfaceError):
            create_connection(db_credentials)


class TestQueryDatabase():
    @pytest.fixture(autouse=True)
    def db_credentials_patch(self):
        with patch("src.processor.utils.transform_data.get_db_credentials") \
                as mock_db_credentials:
            mock_db_credentials.return_value = {
                "DB_USERNAME": "test_username",
                "DB_NAME": "test_name",
                "DB_HOST": "test_host",
                "DB_PASSWORD": "test_password"
            }
            yield mock_db_credentials

    @pytest.fixture(autouse=True)
    def create_connection_patch(self):
        with patch("src.processor.utils.transform_data.create_connection") \
                as mock_create_connection:
            yield mock_create_connection

    @pytest.fixture()
    def test_params(self):
        return ["test_table_name",
                "test_column_name",
                "test_foreign_key",
                "test_foreign_key_value"]

    def test_returns_a_string(self, create_connection_patch, test_params):
        create_connection_patch.return_value.run.return_value = [
            ["test_result"]
        ]
        result = query_database(*test_params)

        assert isinstance(result, str)

    def test_returns_a_single_value(
        self,
        create_connection_patch,
        test_params
    ):
        create_connection_patch.return_value.run.return_value = [
            ["result_one"], ["result_two"], ["result_three"]
        ]
        result = query_database(*test_params)

        assert result == "result_one"


class TestTransformCounterparty():
    @pytest.fixture(autouse=True)
    def query_database_patch(self):
        with patch("src.processor.utils.transform_data.query_database") \
                as mock_query_database:
            mock_query_database.side_effect = [
                '605 Haskell Trafficway',
                'Axel Freeway',
                "County Somewhere",
                'East Bobbie',
                '88253-4257',
                'Heard Island and McDonald Islands',
                '9687 937447'
            ]
            yield mock_query_database

    def test_returns_list_of_dictionaries(self, test_counterparty_data):  # noqa: F811
        test_input_counterparty_data, test_output_counterparty_data = test_counterparty_data

        result = transform_counterparty(test_input_counterparty_data)

        assert isinstance(result, list)

        for item in result:
            assert isinstance(item, dict)

    def test_returns_empty_list_if_passed_file_with_no_data(self):
        assert transform_counterparty([]) == []

    def test_returns_transformed_data(self, test_counterparty_data):  # noqa: F811
        test_input_counterparty_data, test_output_counterparty_data = test_counterparty_data

        result = transform_counterparty(test_input_counterparty_data)
        expected = test_output_counterparty_data

        assert result == expected


class TestTransformStaff():
    @pytest.fixture(autouse=True)
    def query_database_patch(self):
        with patch("src.processor.utils.transform_data.query_database") \
                as mock_query_database:
            mock_query_database.side_effect = [
                "Purchasing",
                "Manchester"
            ]
            yield mock_query_database

    def test_returns_list_of_dictionaries(self, test_staff_data):  # noqa: F811
        test_input_staff_data, test_output_staff_data = test_staff_data

        result = transform_staff(test_input_staff_data)

        assert isinstance(result, list)

        for item in result:
            assert isinstance(item, dict)

    def test_returns_empty_list_if_passed_file_with_no_data(self):
        assert transform_staff([]) == []

    def test_returns_transformed_data(self, test_staff_data):  # noqa: F811
        test_input_staff_data, test_output_staff_data = test_staff_data

        result = transform_staff(test_input_staff_data)
        expected = test_output_staff_data

        assert result == expected


class TestTransformSalesOrder():
    def test_returns_list_of_dictionaries(self, test_sales_data):  # noqa: F811
        test_input_sales_data, test_output_sales_data = test_sales_data

        result = transform_sales_order(test_input_sales_data)

        assert isinstance(result, list)

        for item in result:
            assert isinstance(item, dict)

    def test_returns_empty_list_if_passed_file_with_no_data(
        self,
        test_sales_data  # noqa: F811
    ):
        assert transform_sales_order([]) == []

    def test_returns_transformed_data(self, test_sales_data):  # noqa: F811
        test_input_sales_data, test_output_sales_data = test_sales_data

        result = transform_sales_order(test_input_sales_data)
        expected = test_output_sales_data

        assert result == expected
