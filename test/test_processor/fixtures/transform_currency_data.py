import pytest


@pytest.fixture
def test_currency_data():
    test_input_currency_data = [
        {
            "currency_id": '1',
            "currency_code": 'GBP',
            "created_at": '2022-11-03 14:20:49.962',
            "last_updated": '2022-11-03 14:20:49.962'
        }
    ]
    test_output_currency_data = [
        {
            "currency_id": 1,
            "currency_code": 'GBP',
            "currency_name": "British Pound"
        }
    ]

    return test_input_currency_data, test_output_currency_data
