import pytest
import copy

from unittest.mock import patch, MagicMock
from pg8000.exceptions import InterfaceError

from src.ingestor.utils.fetch_table_names import (
    create_connection,
    flatten_single_subitem_list,
    fetch_table_names
)


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


class TestFlattenSingleSubitemList:
    @pytest.fixture()
    def test_lists(self):
        test_2d_list = [[1], [2], [3]]
        test_flattened_list = [1, 2, 3]

        return test_2d_list, test_flattened_list

    def test_returns_a_one_dimensional_list(self, test_lists):
        test_2d_list, test_flattened_list = test_lists
        result = flatten_single_subitem_list(test_2d_list)

        assert isinstance(result, list)

        for item in result:
            if isinstance(item, list):
                assert False

    def test_returns_an_empty_list_if_passed_an_empty_list(self):
        assert flatten_single_subitem_list([]) == []

    def test_returns_flattened_list(self, test_lists):
        test_2d_list, test_flattened_list = test_lists
        result = flatten_single_subitem_list(test_2d_list)

        assert result == test_flattened_list

    def test_input_data_is_not_mutated(self, test_lists):
        test_2d_list = test_lists
        test_2d_list_original = copy.deepcopy(test_2d_list)

        flatten_single_subitem_list(test_2d_list)

        assert test_2d_list == test_2d_list_original


class TestFetchTableNames:
    @pytest.fixture(autouse=True)
    def test_db_credentials(self):
        mock_env = {
            "DB_USERNAME": "test_username",
            "DB_NAME": "test_name",
            "DB_HOST": "test_host",
            "DB_PASSWORD": "test_password"
        }

        with patch.dict("os.environ", mock_env, clear=True):
            yield {
                "DB_USERNAME": mock_env["DB_USERNAME"],
                "DB_NAME": mock_env["DB_NAME"],
                "DB_HOST": mock_env["DB_HOST"],
                "DB_PASSWORD": mock_env["DB_PASSWORD"],
            }

    @pytest.fixture()
    def test_data(self):
        test_query_result = [['department'], ['staff'], ['transaction']]
        expected_return_data = ['department', 'staff', 'transaction']
        return test_query_result, expected_return_data

    def test_returns_a_list(self, test_data):
        test_query_result = test_data

        with patch("src.ingestor.utils.fetch_table_names.create_connection") \
                as mock_create_connection:
            mock_conn = MagicMock()
            mock_create_connection.return_value = mock_conn

            mock_conn.run.return_value = test_query_result

            result = fetch_table_names(self.test_db_credentials)
            assert isinstance(result, list)

    def test_returns_an_list_if_no_tables_found(self):
        with patch("src.ingestor.utils.fetch_table_names.create_connection") \
                as mock_create_connection:
            mock_conn = MagicMock()
            mock_create_connection.return_value = mock_conn

            mock_conn.run.return_value = []

            result = fetch_table_names(self.test_db_credentials)
            assert result == []

    def test_returns_a_list_of_table_names(self, test_data):
        test_query_result, expected_return_data = test_data

        with patch("src.ingestor.utils.fetch_table_names.create_connection") \
                as mock_create_connection:
            mock_conn = MagicMock()
            mock_create_connection.return_value = mock_conn

            mock_conn.run.return_value = test_query_result

            result = fetch_table_names(self.test_db_credentials)
            assert result == expected_return_data

    def test_raises_an_exception(self):
        with pytest.raises(Exception):
            fetch_table_names(self.test_db_credentials)
