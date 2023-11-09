import pytest


@pytest.fixture
def test_address_data():
    test_input_address_data = [{
        "address_id": '10',
        "address_line_1": '49967 Kaylah Flat',
        "address_line_2": 'Tremaine Circles',
        "district": 'Bedfordshire',
        "city": 'Beaulahcester',
        "postal_code": '89470',
        "country": 'Democratic People\'s Republic of Korea',
        "phone": '4949 998070'
    }]
    test_output_location_data = [{
        "location_id": '10',
        "address_line_1": '49967 Kaylah Flat',
        "address_line_2": 'Tremaine Circles',
        "district": 'Bedfordshire',
        "city": 'Beaulahcester',
        "postal_code": '89470',
        "country": 'Democratic People\'s Republic of Korea',
        "phone": '4949 998070'
    }]

    return test_input_address_data, test_output_location_data
