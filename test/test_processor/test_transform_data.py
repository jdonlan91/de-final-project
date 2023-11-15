import json
import pytest

import boto3
from moto import mock_secretsmanager
from pg8000.exceptions import InterfaceError
from unittest.mock import patch

from src.processor.utils.transform_data import (
    transform_data,
    apply_data_type,
    get_db_credentials,
    create_connection,
    query_database,
    transform_counterparty,
    transform_currency,
    transform_design,
    transform_staff,
    transform_sales_order,
    transform_address,
    # transform_payment,
    transform_purchase_order,
    transform_payment_type,
)

from fixtures.transform_counterparty_data import test_counterparty_data  # noqa: F401,E501
from fixtures.transform_currency_data import test_currency_data  # noqa: F401
from fixtures.transform_design_data import test_design_data  # noqa: F401
from fixtures.transform_staff_data import test_staff_data  # noqa: F401
from fixtures.transform_sales_data import test_sales_data  # noqa: F401
from fixtures.transform_address_data import test_address_data  # noqa: F401
# from fixtures.transform_payment_data import test_payment_data  # noqa: F401
from fixtures.transform_purchase_order_data import test_purchase_order_data  # noqa: F401,E501
from fixtures.transform_payment_type_data import test_payment_type_data  # noqa: F401,E501
# from fixtures.transform_transaction_data import test_transaction_data  # noqa: F401,E501


class TestTransformData:
    @pytest.fixture
    def test_file_name(self):
        return "design/31-10-2023/31-10-2023-152600.csv"

    def test_returns_a_list_of_dictionaries(
        self,
        test_file_name,
        test_design_data  # noqa: F811
    ):
        test_input_design_data, _ = test_design_data
        result = transform_data(test_file_name, test_input_design_data)

        assert isinstance(result, list)

        for item in result:
            assert isinstance(item, dict)

    def test_returns_an_empty_list_if_no_transform_function_found(
        self,
        test_design_data  # noqa: F811
    ):
        test_input_design_data, _ = test_design_data
        result = transform_data("non_existent_table", test_design_data)

        assert result is None

    def test_returns_an_empty_list_if_passed_empty_data(
        self,
        test_file_name
    ):
        result = transform_data(test_file_name, [])

        assert result == []

    @patch("src.processor.utils.transform_data.transform_design")
    def test_calls_the_appropriate_transform_data_function(
        self,
        mock_transform_design,
        test_file_name,
        test_design_data  # noqa: F811
    ):
        test_input_design_data, _ = test_design_data
        transform_data(test_file_name, test_input_design_data)

        assert mock_transform_design.call_count == 1
        assert mock_transform_design.called_with(test_input_design_data)

    def test_returns_transformed_data(
        self,
        test_file_name,
        test_design_data  # noqa: F811
    ):
        test_input_design_data, test_output_design_data = test_design_data
        result = transform_data(test_file_name, test_input_design_data)

        assert result == test_output_design_data


class TestApplyDataType:
    def test_returns_none_when_passed_empty_string(self):
        assert apply_data_type('', int) == ''
        assert apply_data_type('', float) == ''

    def test_returns_an_int(self):
        assert apply_data_type('5', int) == 5

    def test_returns_a_floating_point_number(self):
        assert apply_data_type('2.5', float) == 2.5


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

    def test_returns_list_of_dictionaries(
            self, test_counterparty_data):  # noqa: F811
        (test_input_counterparty_data,
         test_output_counterparty_data) = test_counterparty_data

        result = transform_counterparty(test_input_counterparty_data)

        assert isinstance(result, list)

        for item in result:
            assert isinstance(item, dict)

    def test_returns_empty_list_if_passed_file_with_no_data(self):
        assert transform_counterparty([]) == []

    def test_returns_transformed_data(self,
                                      test_counterparty_data):  # noqa: F811
        (test_input_counterparty_data,
         test_output_counterparty_data) = test_counterparty_data

        result = transform_counterparty(test_input_counterparty_data)
        expected = test_output_counterparty_data

        assert result == expected


class TestTransformCurrency():
    def test_returns_list_of_dictionaries(self,
                                          test_currency_data):  # noqa: F811
        (test_input_currency_data,
         test_output_currency_data) = test_currency_data

        result = transform_currency(test_input_currency_data)

        assert isinstance(result, list)

        for item in result:
            assert isinstance(item, dict)

    def test_returns_empty_list_if_passed_file_with_no_data(
        self,
        test_currency_data  # noqa: F811
    ):
        assert transform_currency([]) == []

    def test_returns_transformed_data(self, test_currency_data):  # noqa: F811
        (test_input_currency_data,
         test_output_currency_data) = test_currency_data
        result = transform_currency(test_input_currency_data)
        expected = test_output_currency_data
        assert result == expected


class TestTransformDesign():
    def test_returns_list_of_dictionaries(self,
                                          test_design_data):  # noqa: F811
        test_input_design_data, test_output_design_data = test_design_data

        result = transform_design(test_input_design_data)

        assert isinstance(result, list)

        for item in result:
            assert isinstance(item, dict)

    def test_returns_empty_list_if_passed_file_with_no_data(
        self,
        test_design_data  # noqa: F811
    ):
        assert transform_design([]) == []

    def test_returns_transformed_data(self, test_design_data):  # noqa: F811
        test_input_design_data, test_output_design_data = test_design_data
        result = transform_design(test_input_design_data)
        expected = test_output_design_data
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


class TestTransformAddress():
    def test_returns_list_of_dictionaries(self,
                                          test_address_data):  # noqa: F811
        test_input_address_data, test_output_location_data = test_address_data

        result = transform_address(test_input_address_data)

        assert isinstance(result, list)

        for item in result:
            assert isinstance(item, dict)

    def test_returns_empty_list_if_passed_file_with_no_data(
        self,
        test_address_data  # noqa: F811
    ):
        assert transform_address([]) == []

    def test_returns_transformed_data(self, test_address_data):  # noqa: F811
        test_input_address_data, test_output_location_data = test_address_data
        result = transform_address(test_input_address_data)
        expected = test_output_location_data
        assert result == expected


# class TestTransformPayment():
#     def test_returns_list_of_dictionaries(
#         self,
#         test_payment_data  # noqa: F811
#     ):
#         test_input_payment_data, test_output_payment_data = test_payment_data

#         result = transform_payment(test_input_payment_data)

#         assert isinstance(result, list)

#         for item in result:
#             assert isinstance(item, dict)

#     def test_returns_empty_list_if_passed_file_with_no_data(
#         self,
#         test_payment_data  # noqa: F811
#     ):
#         assert transform_payment([]) == []

#     def test_returns_transformed_data(self, test_payment_data):  # noqa: F811
#         test_input_payment_data, test_output_payment_data = test_payment_data
#         result = transform_payment(test_input_payment_data)
#         expected = test_output_payment_data
#         assert result == expected


class TestTransformPurchaseOrder():
    def test_returns_list_of_dictionaries(
        self,
        test_purchase_order_data  # noqa: F811
    ):
        test_input_purchase_order_data, test_output_purchase_order_data = test_purchase_order_data  # noqa: 501

        result = transform_purchase_order(test_input_purchase_order_data)

        assert isinstance(result, list)

        for item in result:
            assert isinstance(item, dict)

    def test_returns_empty_list_if_passed_file_with_no_data(
        self,
        test_purchase_order_data  # noqa: F811
    ):
        assert transform_purchase_order([]) == []

    def test_returns_transformed_data(self, test_purchase_order_data):  # noqa: F811,E501
        test_input_purchase_order_data, test_output_purchase_order_data = test_purchase_order_data  # noqa: 501
        result = transform_purchase_order(test_input_purchase_order_data)
        expected = test_output_purchase_order_data
        assert result == expected


class TestTransformPaymentType():
    def test_returns_list_of_dictionaries(
        self,
        test_payment_type_data    # noqa: F811
    ):
        test_input_payment_type_data, test_output_payment_type_data = test_payment_type_data  # noqa: 501

        result = transform_payment_type(test_input_payment_type_data)

        assert isinstance(result, list)

        for item in result:
            assert isinstance(item, dict)

    def test_returns_empty_list_if_passed_file_with_no_data(
        self,
        test_payment_type_data  # noqa: F811
    ):
        assert transform_payment_type([]) == []

    def test_returns_transformed_data(self, test_payment_type_data):  # noqa: 501
        test_input_payment_type_data, test_output_payment_type_data = test_payment_type_data  # noqa: 501
        result = transform_payment_type(test_input_payment_type_data)
        expected = test_output_payment_type_data
        assert result == expected


# class TestTransformTransaction():
#     def test_returns_list_of_dictionaries(
#         self,
#         test_transaction_data  # noqa: F811
#     ):
#         test_input_transaction_data, test_output_transaction_data = test_transaction_data  # noqa: 501

#         result = transform_transaction(test_input_transaction_data)

#         assert isinstance(result, list)

#         for item in result:
#             assert isinstance(item, dict)

    # def test_returns_empty_list_if_passed_file_with_no_data(
    #     self,
    #     test_transaction_data  # noqa: F811
    # ):
    #     assert transform_transaction([]) == []

    # def test_returns_transformed_data(
    #     self,
    #     test_transaction_data  # noqa: F811
    # ):
    #     test_input_transaction_data, test_output_transaction_data = test_transaction_data  # noqa: 501
    #     result = transform_transaction(test_input_transaction_data)
    #     expected = test_output_transaction_data
    #     assert result == expected
