import pytest

from src.processor.utils.transform_data import *


class TestTransformStaff():
    def test_returns_list_of_dictionaries(self, test_staff_data):
        test_input_staff_data, test_output_staff_data = test_staff_data

        result = transform_staff(test_input_staff_data)

        assert isinstance(result, list)

        for item in result:
            assert isinstance(item, dict)

    def test_returns_empty_list_if_passed_file_with_no_data(self):
        assert transform_staff([]) == []

    def test_returns_contents_of_csv_as_list_of_dictionaries(
        self,
        test_staff_data
    ):
        test_input_staff_data, test_output_staff_data = test_staff_data

        result = transform_staff(test_input_staff_data)
        expected = test_output_staff_data

        assert result == expected


class TestTransformSalesOrder():
    def test_returns_list_of_dictionaries(self, test_sales_data):
        test_input_sales_data, test_output_sales_data = test_sales_data

        result = transform_sales_order(test_input_sales_data)

        assert isinstance(result, list)

        for item in result:
            assert isinstance(item, dict)

    def test_returns_empty_list_if_passed_file_with_no_data(self, test_sales_data):
        assert transform_sales_order([]) == []

    def test_returns_contents_of_csv_as_list_of_dictionaries(
        self,
        test_sales_data
    ):
        test_input_sales_data, test_output_sales_data = test_sales_data

        result = transform_sales_order(test_input_sales_data)
        expected = test_output_sales_data

        assert result == expected
