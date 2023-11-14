import pytest


@pytest.fixture
def test_transaction_data():
    test_input_transaction_data = [
        {
            "transaction_id": '1',
            "transaction_type": 'PURCHASE',
            "sales_order_id": '',
            "purchase_order_id": '2',
            "created_at": '2022-11-03 14:20:52.186',
            "last_updated": '2022-11-03 14:20:52.186',
        },
        {
            "transaction_id": '2',
            "transaction_type": 'PURCHASE',
            "sales_order_id": '',
            "purchase_order_id": '3',
            "created_at": '2022-11-03 14:20:52.187',
            "last_updated": '2022-11-03 14:20:52.187',
        }, {
            "transaction_id": '3',
            "transaction_type": 'SALE',
            "sales_order_id": '1',
            "purchase_order_id": '',
            "created_at": '2022-11-03 14:20:52.186',
            "last_updated": '2022-11-03 14:20:52.186',
        }
    ]
    test_output_transaction_data = [
        {
            "transaction_id": 1,
            "transaction_type": 'PURCHASE',
            "sales_order_id": '',
            "purchase_order_id": 2,
        },
        {
            "transaction_id": 2,
            "transaction_type": 'PURCHASE',
            "sales_order_id": '',
            "purchase_order_id": 3,
        }, {
            "transaction_id": 3,
            "transaction_type": 'SALE',
            "sales_order_id": 1,
            "purchase_order_id": '',
        }
    ]

    return test_input_transaction_data, test_output_transaction_data
