import pytest


@pytest.fixture
def test_staff_data():
    test_input_staff_data = [{
        "staff_id": "1",
        "first_name": "Jeremie",
        "last_name": "Franey",
        "department_id": "2",
        "email_address": "jeremie.franey@terrifictotes.com",
        "created_at": "2022-11-03 14:20:51.563",
        "last_updated": "2022-11-03 14:20:51.563"
    }]
    test_output_staff_data = [{
        "staff_id": 1,
        "first_name": "Jeremie",
        "last_name": "Franey",
        "department_name": "Purchasing",
        "location": "Manchester",
        "email_address": "jeremie.franey@terrifictotes.com",
    }]

    return test_input_staff_data, test_output_staff_data
