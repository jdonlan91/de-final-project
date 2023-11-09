import pytest


@pytest.fixture
def test_counterparty_data():
    test_input_counterparty_data = [
        {
            "counterparty_id": '1',
            "counterparty_legal_name": 'Fahey and Sons',
            "legal_address_id": '15',
            "commercial_contact": 'Micheal Toy',
            "delivery_contact": 'Mrs. Lucy Runolfsdottir',
            "created_at": '2022-11-03 14:20:51.563',
            "last_updated": '2022-11-03 14:20:51.563'
        }
    ]
    test_output_counterparty_data = [
        {
            "counterparty_id": '1',
            "counterparty_legal_name": 'Fahey and Sons',
            "counterparty_legal_address_line_1": '605 Haskell Trafficway',
            "counterparty_legal_address_line_2": 'Axel Freeway',
            "counterparty_legal_district": "County Somewhere",
            "counterparty_legal_city": 'East Bobbie',
            "counterparty_legal_postal_code": '88253-4257',
            "counterparty_legal_country": 'Heard Island and McDonald Islands',
            "counterparty_legal_phone_number": '9687 937447'
        }
    ]

    return test_input_counterparty_data, test_output_counterparty_data
