import pytest


@pytest.fixture
def test_payment_type_data():
    test_input_payment_type_data = [
        {
            "payment_type_id": '1',
            "payment_type_name": 'SALES_RECEIPT',
            "created_at": '2022-11-03 14:20:49.962',
            "last_updated": '2022-11-03 14:20:49.962'
        },
        {
            "payment_type_id": '2',
            "payment_type_name": 'SALES_REFUND',
            "created_at": '2022-11-03 14:20:49.962',
            "last_updated": '2022-11-03 14:20:49.962'
        },
        {
            "payment_type_id": '3',
            "payment_type_name": 'PURCHASE_PAYMENT',
            "created_at": '2022-11-03 14:20:49.962',
            "last_updated": '2022-11-03 14:20:49.962'
        },
        {
            "payment_type_id": '4',
            "payment_type_name": 'PURCHASE_REFUND',
            "created_at": '2022-11-03 14:20:49.962',
            "last_updated": '2022-11-03 14:20:49.962'
        }
    ]
    test_output_payment_type_data = [
        {
            "payment_type_id": 1,
            "payment_type_name": 'SALES_RECEIPT'
        },
        {
            "payment_type_id": 2,
            "payment_type_name": 'SALES_REFUND'
        },
        {
            "payment_type_id": 3,
            "payment_type_name": 'PURCHASE_PAYMENT'
        },
        {
            "payment_type_id": 4,
            "payment_type_name": 'PURCHASE_REFUND'
        }
    ]

    return test_input_payment_type_data, test_output_payment_type_data
