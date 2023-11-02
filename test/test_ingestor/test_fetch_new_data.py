import pytest
import copy
from datetime import datetime

from unittest.mock import patch, MagicMock
from pg8000.exceptions import DatabaseError

from src.ingestor.utils.fetch_new_data import (
    create_connection,
    convert_lists_to_dicts,
    fetch_new_data
)


class TestCreateConnection:
    def test_create_connection_failure(self):
        db_credentials = {
            "DB_USERNAME": "invalid_user",
            "DB_PASSWORD": "invalid_password",
            "DB_HOST": "localhost",
            "DB_NAME": "invalid_db",
        }

        with pytest.raises(DatabaseError):
            create_connection(db_credentials)


class TestConvertListsToDictionaries():
    @pytest.fixture
    def test_lists(self):
        test_list_of_keys = ["id", "first_name", "last_name"]
        test_list_of_lists = [
            [1, "Jeremie", "Franey"],
            [2, "Deron", "Beier"],
            [3, "Jeanette", "Erdman"]
        ]
        test_list_of_dicts = [
            {"id": 1, "first_name": "Jeremie", "last_name": "Franey"},
            {"id": 2, "first_name": "Deron", "last_name": "Beier"},
            {"id": 3, "first_name": "Jeanette", "last_name": "Erdman"}
        ]
        return test_list_of_keys, test_list_of_lists, test_list_of_dicts

    def test_returns_an_empty_list_if_passed_at_least_one_empty_list(self):
        test_list_of_keys = self.test_lists

        assert convert_lists_to_dicts([], []) == []
        assert convert_lists_to_dicts([], test_list_of_keys) == []

    def test_returns_list_of_dictionaries(self, test_lists):
        test_list_of_keys, test_list_of_lists, test_list_of_dicts = test_lists

        expected = test_list_of_dicts
        result = convert_lists_to_dicts(test_list_of_lists, test_list_of_keys)

        assert expected == result

    def test_input_data_is_not_mutated(self, test_lists):
        test_list_of_keys, test_list_of_lists, test_list_of_dicts = test_lists

        test_list_of_keys_original = copy.deepcopy(test_list_of_keys)
        test_list_of_lists_original = copy.deepcopy(test_list_of_lists)

        expected = test_list_of_dicts
        result = convert_lists_to_dicts(test_list_of_lists, test_list_of_keys)

        assert test_list_of_keys == test_list_of_keys_original
        assert test_list_of_lists == test_list_of_lists_original
        assert expected == result


class TestFetchNewData:
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

    @pytest.fixture
    def test_timestamp(self):
        return datetime(2023, 1, 1, 14, 20, 51, 563000)

    @pytest.fixture
    def test_data(self):
        test_columns = ["id", "first_name", "last_name"]
        new_staff_data = [
            [1, "Jeremie", "Franey"],
            [2, "Deron", "Beier"],
            [3, "Jeanette", "Erdman"]
        ]
        expected_return_data = [
            {"id": 1, "first_name": "Jeremie", "last_name": "Franey"},
            {"id": 2, "first_name": "Deron", "last_name": "Beier"},
            {"id": 3, "first_name": "Jeanette", "last_name": "Erdman"}
        ]
        return test_columns, new_staff_data, expected_return_data

    def test_if_no_new_data_returns_empty_list(self):
        with patch("src.ingestor.utils.fetch_new_data.create_connection") \
                as mock_create_connection:
            mock_conn = MagicMock()
            mock_create_connection.return_value = mock_conn

            mock_conn.run.return_value = []

            result = fetch_new_data(
                "staff",
                self.test_timestamp,
                self.test_db_credentials
            )
            assert result == []

    def test_returns_list_of_dictionaries_if_new_data_found(self, test_data):
        test_columns, new_staff_data, expected_return_data = test_data

        with patch("src.ingestor.utils.fetch_new_data.create_connection") \
                as mock_create_connection:
            mock_conn = MagicMock()
            mock_create_connection.return_value = mock_conn

            mock_conn.run.return_value = new_staff_data
            mock_conn.columns = [
                {'name': column_name} for column_name in test_columns
            ]

            result = fetch_new_data(
                "staff",
                self.test_timestamp,
                self.test_db_credentials
            )

            assert result == expected_return_data

    def test_raises_an_error(self):
        with pytest.raises(Exception):
            fetch_new_data(
                "staff",
                self.test_timestamp,
                self.test_db_credentials
            )
