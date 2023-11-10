from src.ingestor.utils.convert_to_csv import convert_to_csv
import pytest


def test_return_a_string():
    input = [{"staff_id": 1, "first_name": "Jeremie"}]
    expected = True
    assert isinstance(convert_to_csv(input), str) == expected


def test_returns_an_empty_string_when_empty_list_passed():
    assert convert_to_csv([]) == ""


def test_does_not_mutate_passed_list():
    input = [{"staff_id": 1, "first_name": "Jeremie"}]
    convert_to_csv(input)
    assert input == [{"staff_id": 1, "first_name": "Jeremie"}]


def test_converts_list_of_one_dictionary_to_csv_string():
    input = [{"staff_id": 1, "first_name": "Jeremie"}]
    expected = "staff_id,first_name\n1,Jeremie"
    assert convert_to_csv(input) == expected


def test_conver_list_of_mult_dictionaries_with_2_columns_to_csv_string():
    input = [
        {"staff_id": 1, "first_name": "Jeremie"},
        {"staff_id": 2, "first_name": "Peter"},
        {"staff_id": 3, "first_name": "Steve"},
        {"staff_id": 4, "first_name": "Mary"},
    ]
    expected = "staff_id,first_name\n1,Jeremie\n2,Peter\n3,Steve\n4,Mary"
    assert convert_to_csv(input) == expected


def test_conver_list_of_mult_dictionaries_with_mult_columns_to_csv_string():
    input = [
        {
            "staff_id": 1,
            "first_name": "Jeremie",
            "last_name": "Franey",
            "dep_id": 2,
            "email_address": "jeremie.franey@terrifictotes.com",
            "created_at": "2022-11-03 14:20:51.563",
        },
        {
            "staff_id": 2,
            "first_name": "Deron",
            "last_name": "Beier",
            "dep_id": 6,
            "email_address": "deron.beier@terrifictotes.com",
            "created_at": "2022-11-03 14:20:51.563",
        },
        {
            "staff_id": 3,
            "first_name": "Jeanette",
            "last_name": "Erdman",
            "dep_id": 6,
            "email_address": "jeanette.erdman@terrifictotes.com",
            "created_at": "2022-11-03 14:20:51.563",
        }
    ]
    expected = """staff_id,first_name,last_name,dep_id,email_address,created_at
1,Jeremie,Franey,2,jeremie.franey@terrifictotes.com,2022-11-03 14:20:51.563
2,Deron,Beier,6,deron.beier@terrifictotes.com,2022-11-03 14:20:51.563
3,Jeanette,Erdman,6,jeanette.erdman@terrifictotes.com,2022-11-03 14:20:51.563"""
    assert convert_to_csv(input) == expected


def test_raises_an_error():
    with pytest.raises(Exception):
        convert_to_csv(1)
