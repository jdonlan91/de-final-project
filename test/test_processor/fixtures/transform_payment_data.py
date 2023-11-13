import pytest


@pytest.fixture
def test_payment_data():
    test_input_payment_data = [
        {
            "payment_id": '2',
            "created_at": '2022-11-03 14:20:52.187',
            "last_updated": '2022-11-03 14:20:52.187',
            "transaction_id": '2',
            "counterparty_id": '15',
            "payment_amount": '552548.62',
            "currency_id": '2',
            "payment_type_id": '3',
            "paid": 'false',
            "payment_date": '2022-11-04',
            "company_ac_number": '67305075',
            "counterparty_ac_number": '31622269',
        },
        {
            "payment_id": '3',
            "created_at": '2022-11-03 14:20:52.186',
            "last_updated": '2022-11-03 14:20:52.186',
            "transaction_id": '3',
            "counterparty_id": '18',
            "payment_amount": '205952.22',
            "currency_id": '3',
            "payment_type_id": '1',
            "paid": 'false',
            "payment_date": '2022-11-03',
            "company_ac_number": '81718079',
            "counterparty_ac_number": '47839086',
        }, {
            "payment_id": '5',
            "created_at": '2022-11-03 14:20:52.187',
            "last_updated": '2022-11-03 14:20:52.187',
            "transaction_id": '5',
            "counterparty_id": '17',
            "payment_amount": '57067.20',
            "currency_id": '2',
            "payment_type_id": '3',
            "paid": 'false',
            "payment_date": '2022-11-06',
            "company_ac_number": '66213052',
            "counterparty_ac_number": '91659548',
        }
    ]
    test_output_payment_data = [
        {
            "payment_id": 2,
            "created_date": '2022-11-03',
            "created_time": '14:20:52.187',
            "last_updated_date": '2022-11-03',
            "last_updated_time": '14:20:52.187',
            "transaction_id": 2,
            "counterparty_id": 15,
            "payment_amount": 552548.62,
            "currency_id": 2,
            "payment_type_id": 3,
            "paid": False,
            "payment_date": '2022-11-04'
        },
        {
            "payment_id": 3,
            "created_date": '2022-11-03',
            "created_time": '14:20:52.186',
            "last_updated_date": '2022-11-03',
            "last_updated_time": '14:20:52.186',
            "transaction_id": 3,
            "counterparty_id": 18,
            "payment_amount": 205952.22,
            "currency_id": 3,
            "payment_type_id": 1,
            "paid": False,
            "payment_date": '2022-11-03'
        }, {
            "payment_id": 5,
            "created_date": '2022-11-03',
            "created_time": '14:20:52.187',
            "last_updated_date": '2022-11-03',
            "last_updated_time": '14:20:52.187',
            "transaction_id": 5,
            "counterparty_id": 17,
            "payment_amount": 57067.20,
            "currency_id": 2,
            "payment_type_id": 3,
            "paid": False,
            "payment_date": '2022-11-06'
        }
    ]

    return test_input_payment_data, test_output_payment_data
