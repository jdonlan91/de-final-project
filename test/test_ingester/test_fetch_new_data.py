from dotenv import load_dotenv
from src.ingester.utils.fetch_new_data import fetch_new_data
import pytest
from os import environ
from datetime import datetime
from pg8000.exceptions import DatabaseError


@pytest.fixture
def db_credentials():
    load_dotenv()
    return {
        "DB_USERNAME": environ["DB_USERNAME"],
        "DB_NAME": environ["DB_NAME"],
        "DB_HOST": environ["DB_HOST"],
        "DB_PASSWORD": environ["DB_PASSWORD"],
    }


@pytest.fixture
def three_rows_from_staff():
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
        },
    ]


def test_if_no_new_data_returns_empty_list(db_credentials):
    assert (
        fetch_new_data(
            "staff", datetime(2023, 1, 1, 14, 20, 51, 563000), db_credentials
        )
        == []
    )


def test_if_table_contains_new_data_returns_list_of_dictionaries(
    db_credentials, three_rows_from_staff
):
    test_table_name = "staff"
    test_timestamp = datetime(2021, 1, 1, 14, 20, 51, 563000)
    output = fetch_new_data(test_table_name, test_timestamp, db_credentials)
    assert output[:3] == three_rows_from_staff


def test_raises_error_if_cannot_connect_to_database(db_credentials):
    db_credentials["DB_PASSWORD"] = "12345"
    test_table_name = "staff"
    test_timestamp = datetime(2021, 1, 1, 14, 20, 51, 563000)
    with pytest.raises(DatabaseError):
        fetch_new_data(test_table_name, test_timestamp, db_credentials)


def test_raises_error_if_table_does_not_exist(db_credentials):
    test_table_name = "invalid_table_name"
    test_timestamp = datetime(2021, 1, 1, 14, 20, 51, 563000)
    with pytest.raises(DatabaseError):
        fetch_new_data(test_table_name, test_timestamp, db_credentials)
