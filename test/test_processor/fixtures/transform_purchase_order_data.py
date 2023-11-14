import pytest


@pytest.fixture
def test_purchase_order_data():
    test_input_purchase_order_data = [
        {
            "purchase_order_id": 1,
            "created_at": '2022-11-03 14:20:52.187',
            "last_updated": '2022-11-03 14:20:52.187',
            "staff_id": '12',
            "counterparty_id": '11',
            "item_code": 'ZDOI5EA',
            "item_quantity": '371',
            "item_unit_price": '361.39',
            "currency_id": '2',
            "agreed_delivery_date": '2022-11-09',
            "agreed_payment_date": '2022-11-07',
            "agreed_delivery_location_id": '6',
        },
        {
            "purchase_order_id": 2,
            "created_at": '2022-11-03 14:20:52.186',
            "last_updated": '2022-11-03 14:20:52.186',
            "staff_id": '20',
            "counterparty_id": '17',
            "item_code": 'QLZLEXR',
            "item_quantity": '286',
            "item_unit_price": '199.04',
            "currency_id": '2',
            "agreed_delivery_date": '2022-11-04',
            "agreed_payment_date": '2022-11-07',
            "agreed_delivery_location_id": '6',
        }, {
            "purchase_order_id": '3',
            "created_at": '2022-11-03 14:20:52.187',
            "last_updated": '2022-11-03 14:20:52.187',
            "staff_id": '12',
            "counterparty_id": '15',
            "item_code": 'AN3D85L',
            "item_quantity": '839',
            "item_unit_price": '658.58',
            "currency_id": '2',
            "agreed_delivery_date": '2022-11-05',
            "agreed_payment_date": '2022-11-04',
            "agreed_delivery_location_id": '6',
        }
    ]
    test_output_purchase_order_data = [
        {
            "purchase_order_id": 1,
            "created_date": '2022-11-03',
            "created_time": '14:20:52.187',
            "last_updated_date": '2022-11-03',
            "last_updated_time": '14:20:52.187',
            "staff_id": 12,
            "counterparty_id": 11,
            "item_code": 'ZDOI5EA',
            "item_quantity": 371,
            "item_unit_price": 361.39,
            "currency_id": 2,
            "agreed_delivery_date": '2022-11-09',
            "agreed_payment_date": '2022-11-07',
            "agreed_delivery_location_id": 6,
        },
        {
            "purchase_order_id": 2,
            "created_date": '2022-11-03',
            "created_time": '14:20:52.186',
            "last_updated_date": '2022-11-03',
            "last_updated_time": '14:20:52.186',
            "staff_id": 20,
            "counterparty_id": 17,
            "item_code": 'QLZLEXR',
            "item_quantity": 286,
            "item_unit_price": 199.04,
            "currency_id": 2,
            "agreed_delivery_date": '2022-11-04',
            "agreed_payment_date": '2022-11-07',
            "agreed_delivery_location_id": 6,
        }, {
            "purchase_order_id": 3,
            "created_date": '2022-11-03',
            "created_time": '14:20:52.187',
            "last_updated_date": '2022-11-03',
            "last_updated_time": '14:20:52.187',
            "staff_id": 12,
            "counterparty_id": 15,
            "item_code": 'AN3D85L',
            "item_quantity": 839,
            "item_unit_price": 658.58,
            "currency_id": 2,
            "agreed_delivery_date": '2022-11-05',
            "agreed_payment_date": '2022-11-04',
            "agreed_delivery_location_id": 6,
        }
    ]

    return test_input_purchase_order_data, test_output_purchase_order_data
