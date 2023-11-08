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
        "staff_id": "1",
        "first_name": "Jeremie",
        "last_name": "Franey",
        "department_name": "Purchasing",
        "location": "Manchester",
        "email_address": "jeremie.franey@terrifictotes.com",
    }]

    return test_input_staff_data, test_output_staff_data


@pytest.fixture
def test_sales_data():
    test_input_sales_data = [{
        "sales_order_id": "1",
        "created_at": "2022-11-03 14:20:52.186",
        "last_updated": "2022-11-03 14:20:52.186",
        "design_id": "9",
        "staff_id": "16",
        "counterparty_id": "18",
        "units_sold": "84754",
        "unit_price": "2.43",
        "currency_id": "3",
        "agreed_delivery_date": "2022-11-10",
        "agreed_payment_date": "2022-11-03",
        "agreed_delivery_location_id": "4",
    }, {
        "sales_order_id": "2",
        "created_at": "2022-11-04 15:21:23.586",
        "last_updated": "2022-11-04 15:21:23.586",
        "design_id": "3",
        "staff_id": "12",
        "counterparty_id": "15",
        "units_sold": "38564",
        "unit_price": "1.89",
        "currency_id": "3",
        "agreed_delivery_date": "2022-11-20",
        "agreed_payment_date": "2022-11-13",
        "agreed_delivery_location_id": "4",
    }]
    test_output_sales_data = [{
        "sales_order_id": "1",
        "created_date": "2022-11-03",
        "created_time": "14:20:52.186",
        "last_updated_date": "2022-11-03",
        "last_updated_time": "14:20:52.186",
        "sales_staff_id": "16",
        "counterparty_id": "18",
        "units_sold": "84754",
        "unit_price": "2.43",
        "currency_id": "3",
        "design_id": "9",
        "agreed_payment_date": "2022-11-03",
        "agreed_delivery_date": "2022-11-10",
        "agreed_delivery_location_id": "4",
    }, {
        "sales_order_id": "2",
        "created_date": "2022-11-04",
        "created_time": "15:21:23.586",
        "last_updated_date": "2022-11-04",
        "last_updated_time": "15:21:23.586",
        "sales_staff_id": "12",
        "counterparty_id": "15",
        "units_sold": "38564",
        "unit_price": "1.89",
        "currency_id": "3",
        "design_id": "3",
        "agreed_payment_date": "2022-11-13",
        "agreed_delivery_date": "2022-11-20",
        "agreed_delivery_location_id": "4",
    }]

    return test_input_sales_data, test_output_sales_data
