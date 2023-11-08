import json

import boto3
from pg8000.native import Connection, identifier, literal


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


# def transform_counterparty():
#     pass


# def transform_currency():
#     pass


# def transform_department():
#     pass


# def transform_design():
#     pass


def transform_staff(data):
    transformed_data = [
        {
            "staff_id": row["staff_id"],
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
            "sales_order_id": row["sales_order_id"],
            "created_date": row["created_at"][:10],
            "created_time": row["created_at"][11:],
            "last_updated_date": row["last_updated"][:10],
            "last_updated_time": row["last_updated"][11:],
            "sales_staff_id": row["staff_id"],
            "counterparty_id": row["counterparty_id"],
            "units_sold": row["units_sold"],
            "unit_price": row["unit_price"],
            "currency_id": row["currency_id"],
            "design_id": row["design_id"],
            "agreed_payment_date": row["agreed_payment_date"],
            "agreed_delivery_date": row["agreed_delivery_date"],
            "agreed_delivery_location_id": row["agreed_delivery_location_id"]
        }
        for row in data
    ]

    return transformed_data


# def transform_address():
#     pass


# def transform_payment():
#     pass


# def transform_purchase_order():
#     pass


# def transform_payment_type():
#     pass


# def transform_transaction():
#     pass

transformed_data = transform_staff([{
    "staff_id": "1",
    "first_name": "Jeremie",
    "last_name": "Franey",
    "department_id": "2",
    "email_address": "jeremie.franey@terrifictotes.com",
    "created_at": "2022-11-03 14:20:51.563",
    "last_updated": "2022-11-03 14:20:51.563"
}])

print(transformed_data)
