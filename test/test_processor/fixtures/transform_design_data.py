import pytest


@pytest.fixture
def test_design_data():
    test_input_design_data = [
        {
            "design_id": "8",
            "created_at": '2022-11-03 14:20:49.962',
            "design_name": "Wooden",
            "file_location": '/usr',
            'file_name': 'wooden-20220717-npgz.json',
            'last_updated': '2022-11-03 14:20:49.962'
        }
    ]
    test_output_design_data = [
        {
            "design_id": 8,
            "design_name": "Wooden",
            "file_location": '/usr',
            'file_name': 'wooden-20220717-npgz.json'
        }
    ]

    return test_input_design_data, test_output_design_data
