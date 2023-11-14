import json

import ccy
import boto3
from pg8000.native import Connection, identifier, literal


def transform_data(file_name, data):
    transform_to_apply = "transform_" + file_name.split('/')[0]
    transformed_data = globals()[transform_to_apply](data)

    return transformed_data


def apply_data_type(string, data_type):
    if string == '':
        return ''
    elif data_type == int:
        return int(string)
    elif data_type == float:
        return float(string)


def get_db_credentials():
    secret_name = "totesys_db_credentials"
    region_name = "eu-west-2"

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager",
                            region_name=region_name)

    get_secret_value_response = client.get_secret_value(SecretId=secret_name)

    secret = json.loads(get_secret_value_response["SecretString"])
    db_credentials = {}
    db_credentials["DB_HOST"] = secret["host"]
    db_credentials["DB_USERNAME"] = secret["username"]
    db_credentials["DB_PASSWORD"] = secret["password"]
    db_credentials["DB_NAME"] = secret["dbname"]

    return db_credentials


def create_connection(db_credentials):
    return Connection(
        user=db_credentials["DB_USERNAME"],
        password=db_credentials["DB_PASSWORD"],
        host=db_credentials["DB_HOST"],
        database=db_credentials["DB_NAME"],
    )


def query_database(table_name, column_name, foreign_key, foreign_key_value):
    db_credentials = get_db_credentials()
    conn = create_connection(db_credentials)

    query = f"""
        SELECT {identifier(column_name)}
        FROM {identifier(table_name)}
        WHERE {identifier(foreign_key)} = {literal(foreign_key_value)}
    """

    query_result = conn.run(query)

    return query_result[0][0]


def transform_counterparty(data):
    transformed_data = [
        {
            "counterparty_id": apply_data_type(row["counterparty_id"], int),
            "counterparty_legal_name": row["counterparty_legal_name"],
            "counterparty_legal_address_line_1": query_database(
                table_name="address",
                column_name="address_line_1",
                foreign_key="address_id",
                foreign_key_value=row["legal_address_id"]
            ),
            "counterparty_legal_address_line_2": query_database(
                table_name="address",
                column_name="address_line_2",
                foreign_key="address_id",
                foreign_key_value=row["legal_address_id"]
            ),
            "counterparty_legal_district": query_database(
                table_name="address",
                column_name="district",
                foreign_key="address_id",
                foreign_key_value=row["legal_address_id"]
            ),
            "counterparty_legal_city": query_database(
                table_name="address",
                column_name="city",
                foreign_key="address_id",
                foreign_key_value=row["legal_address_id"]
            ),
            "counterparty_legal_postal_code": query_database(
                table_name="address",
                column_name="district",
                foreign_key="postal_code",
                foreign_key_value=row["legal_address_id"]
            ),
            "counterparty_legal_country": query_database(
                table_name="address",
                column_name="country",
                foreign_key="address_id",
                foreign_key_value=row["legal_address_id"]
            ),
            "counterparty_legal_phone_number": query_database(
                table_name="address",
                column_name="phone",
                foreign_key="address_id",
                foreign_key_value=row["legal_address_id"]
            )
        }
        for row in data
    ]

    return transformed_data


def transform_currency(data):
    transformed_data = [
        {
            "currency_id": apply_data_type(row["currency_id"], int),
            "currency_code": row["currency_code"],
            "currency_name": ccy.currency(row["currency_code"]).name
        }
        for row in data
    ]

    return transformed_data


def transform_design(data):
    transformed_data = [
        {
            "design_id": apply_data_type(row["design_id"], int),
            "design_name": row["design_name"],
            "file_location": row["file_location"],
            "file_name": row["file_name"]
        }
        for row in data
    ]

    return transformed_data


def transform_staff(data):
    transformed_data = [
        {
            "staff_id": apply_data_type(row["staff_id"], int),
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "department_name": query_database(
                table_name="department",
                column_name="department_name",
                foreign_key="department_id",
                foreign_key_value=row["department_id"]
            ),
            "location": query_database(
                table_name="department",
                column_name="location",
                foreign_key="department_id",
                foreign_key_value=row["department_id"]
            ),
            "email_address": row["email_address"]
        }
        for row in data
    ]

    return transformed_data


def transform_sales_order(data):
    transformed_data = [
        {
            "sales_order_id": apply_data_type(row["sales_order_id"], int),
            "created_date": row["created_at"][:10],
            "created_time": row["created_at"][11:],
            "last_updated_date": row["last_updated"][:10],
            "last_updated_time": row["last_updated"][11:],
            "sales_staff_id": apply_data_type(row["staff_id"], int),
            "counterparty_id": apply_data_type(row["counterparty_id"], int),
            "units_sold": apply_data_type(row["units_sold"], int),
            "unit_price": apply_data_type(row["unit_price"], float),
            "currency_id": apply_data_type(row["currency_id"], int),
            "design_id": apply_data_type(row["design_id"], int),
            "agreed_payment_date": row["agreed_payment_date"],
            "agreed_delivery_date": row["agreed_delivery_date"],
            "agreed_delivery_location_id": apply_data_type(
                row["agreed_delivery_location_id"],
                int
            )
        }
        for row in data
    ]

    return transformed_data


def transform_address(data):
    transformed_data = [
        {
            "location_id": apply_data_type(row["address_id"], int),
            "address_line_1": row["address_line_1"],
            "address_line_2": row["address_line_2"],
            "district": row["district"],
            "city": row["city"],
            "postal_code": row["postal_code"],
            "country": row["country"],
            "phone": row["phone"],
        }
        for row in data
    ]

    return transformed_data


def transform_payment(data):
    transformed_data = [
        {
            "payment_id": apply_data_type(row["payment_id"], int),
            "created_date": row["created_at"][:10],
            "created_time": row["created_at"][11:],
            "last_updated_date": row["last_updated"][:10],
            "last_updated_time": row["last_updated"][11:],
            "transaction_id": apply_data_type(row["transaction_id"], int),
            "counterparty_id": apply_data_type(row["counterparty_id"], int),
            "payment_amount": apply_data_type(row["payment_amount"], float),
            "currency_id": apply_data_type(row["currency_id"], int),
            "payment_type_id": apply_data_type(row["payment_type_id"], int),
            "paid": row["paid"],
            "payment_date": row["payment_date"]
        }
        for row in data
    ]

    return transformed_data


def transform_purchase_order(data):
    transformed_data = [
        {
            "purchase_order_id": apply_data_type(
                row["purchase_order_id"],
                int
            ),
            "created_date": row["created_at"][:10],
            "created_time": row["created_at"][11:],
            "last_updated_date": row["last_updated"][:10],
            "last_updated_time": row["last_updated"][11:],
            "staff_id": apply_data_type(row["staff_id"], int),
            "counterparty_id": apply_data_type(row["counterparty_id"], int),
            "item_code": row["item_code"],
            "item_quantity": apply_data_type(row["item_quantity"], int),
            "item_unit_price": float(row["item_unit_price"]),
            "currency_id": apply_data_type(row["currency_id"], int),
            "agreed_delivery_date": row["agreed_delivery_date"],
            "agreed_payment_date": row["agreed_payment_date"],
            "agreed_delivery_location_id": apply_data_type(
                row["agreed_delivery_location_id"],
                int
            )
        }
        for row in data
    ]

    return transformed_data


def transform_payment_type(data):
    transformed_data = [
        {
            "payment_type_id": apply_data_type(row["payment_type_id"], int),
            "payment_type_name": row["payment_type_name"],
        }
        for row in data
    ]

    return transformed_data


def transform_transaction(data):
    transformed_data = [
        {
            "transaction_id": apply_data_type(row["transaction_id"], int),
            "transaction_type": row["transaction_type"],
            "sales_order_id": apply_data_type(row["sales_order_id"], int),
            "purchase_order_id": apply_data_type(
                row["purchase_order_id"],
                int
            )
        }
        for row in data
    ]

    return transformed_data


def transform_department(data):
    pass
