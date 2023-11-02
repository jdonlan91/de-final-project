import pytest
import copy
from os import environ
from datetime import datetime

from dotenv import load_dotenv
from unittest.mock import patch
from pg8000.exceptions import DatabaseError

from src.ingestor.utils.fetch_new_data import fetch_new_data, convert_lists_to_dicts


@pytest.fixture(autouse=True)
def test_db_credentials():
    mock_env = {
        "DB_USERNAME": "test_username",
        "DB_NAME": "test_name",
        "DB_HOST": "test_host",
        "DB_PASSWORD": "test_password",
    }

    with patch.dict("os.environ", mock_env, clear=True):
        return {
            "DB_USERNAME": mock_env["DB_USERNAME"],
            "DB_NAME": mock_env["DB_NAME"],
            "DB_HOST": mock_env["DB_HOST"],
            "DB_PASSWORD": mock_env["DB_PASSWORD"],
        }


@pytest.fixture
def db_credentials():
    load_dotenv()
    return {
        "DB_USERNAME": environ["DB_USERNAME"],
        "DB_NAME": environ["DB_NAME"],
        "DB_HOST": environ["DB_HOST"],
        "DB_PASSWORD": environ["DB_PASSWORD"],
    }


@pytest.fixture(autouse=True)
def test_timestamp():
    return datetime(2023, 1, 1, 14, 20, 51, 563000)


@pytest.fixture
def new_staff_data():
    return [
        {
            "staff_id": 1,
            "first_name": "Jeremie",
            "last_name": "Franey",
            "department_id": 2,
            "email_address": "jeremie.franey@terrifictotes.com",
            "created_at": "2022-11-03 14:20:51.563",
            "last_updated": "2022-11-03 14:20:51.563",
        },
        {
            "staff_id": 2,
            "first_name": "Deron",
            "last_name": "Beier",
            "department_id": 6,
            "email_address": "deron.beier@terrifictotes.com",
            "created_at": "2022-11-03 14:20:51.563",
            "last_updated": "2022-11-03 14:20:51.563",
        },
        {
            "staff_id": 3,
            "first_name": "Jeanette",
            "last_name": "Erdman",
            "department_id": 6,
            "email_address": "jeanette.erdman@terrifictotes.com",
            "created_at": "2022-11-03 14:20:51.563",
            "last_updated": "2022-11-03 14:20:51.563",
        }
    ]


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

    def test_returns_an_empty_list_if_passed_at_least_one_empty_list(self, test_lists):
        test_list_of_keys = test_lists

        assert convert_lists_to_dicts([], []) == []
        assert convert_lists_to_dicts([], test_list_of_keys) == []

    def test_returns_list_of_dictionaries(
        self,
        test_lists
    ):
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
    def test_if_no_new_data_returns_empty_list(self, test_db_credentials):
        with patch("src.ingestor.utils.fetch_new_data.create_connection") as mock_create_connection:
            mock_connection = mock_create_connection.return_value
            mock_connection.run.return_value = []

            result = fetch_new_data(
                "staff", test_timestamp, test_db_credentials)
            assert result == []

    def test_if_table_contains_new_data_returns_list_of_dictionaries(
        self, db_credentials,
        new_staff_data
    ):
        # with patch("src.ingestor.utils.fetch_new_data.create_connection") as mock_create_connection:
        #     mock_connection = mock_create_connection.return_value
        #     mock_connection.run.return_value = new_staff_data

        #     result = fetch_new_data("staff", test_timestamp, db_credentials)
        #     print(f'query result: {result}')
        #     assert result == new_staff_data

        test_table_name = "staff"
        test_timestamp = datetime(2021, 1, 1, 14, 20, 51, 563000)
        result = fetch_new_data(
            test_table_name, test_timestamp, db_credentials)
        assert result[:3] == new_staff_data

    def test_raises_error_if_cannot_connect_to_database(self, db_credentials):
        db_credentials["DB_PASSWORD"] = "12345"
        test_table_name = "staff"

        with pytest.raises(DatabaseError):
            fetch_new_data(test_table_name, test_timestamp, db_credentials)

    def test_raises_error_if_table_does_not_exist(self, db_credentials):
        test_table_name = "invalid_table_name"

        with pytest.raises(DatabaseError):
            fetch_new_data(test_table_name, test_timestamp, db_credentials)
